// gcc sensorslog.c -s -O3 -lwiringPi -lrt -o senslog
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <limits.h>
#include <wiringPi.h>
#include <pwd.h>
#include <sys/stat.h>

#define PIRPIN 7
#define BUTTONPIN 3
#define PATH "/data/"
#define SOCKETPATH "/tmp/alarm_button"
#define USER "root"

#define DEBUG 1
#define debug_print(fmt, ...) \
                do { if (DEBUG) fprintf(stderr, fmt, __VA_ARGS__); } while (0)

// timezone offset
long int tzoffset = 0;

// file info for PIR detector
char pirfilename[PATH_MAX] = {0};
int pirfilesize = 0;

// file info for button
char btnfilename[PATH_MAX] = {0};
int btnfilesize = 0;

double getTimestamp()
{
    // get Epoch in javascript format (*1000) with microsecond
    struct timespec tim;
    clock_gettime(CLOCK_REALTIME, &tim);
    double s = tim.tv_sec + tzoffset;
    s = s * 1000; // convert in ms
    long m = tim.tv_nsec;
    m = m / 1000000; // convert in ms
    s = s + m;
    return s;
}

void setLine(char *buffer, size_t buf_size, double timestamp, int value)
{
    snprintf(buffer, buf_size, "%0.0lf,%d\n", timestamp, value);
}

void setFilename(char *filename, size_t buf_size, double timestamp, char* extension)
{
    struct passwd *pw = getpwuid(getuid());
    const char *homedir = pw->pw_dir;
    debug_print("%s%s%0.0lf.%s\n", homedir, PATH, timestamp, extension);
    snprintf(filename, buf_size, "%s%s%0.0lf.%s", homedir, PATH, timestamp, extension);
}

long appendToFile(char *filename, char* line)
{
    debug_print("appendToFile %s\n",filename);
    FILE *fp = fopen(filename, "a");
    size_t len = strlen(line);
    fwrite(line, sizeof(char), len, fp);
    long size = ftell(fp);
    fclose(fp);
    return size;
}

void mouvement()
{
    double timestamp = getTimestamp();
    int d = digitalRead(PIRPIN);

    char line[32];
    setLine(line, sizeof(line), timestamp, d);

    if (pirfilesize == 0
    ||  pirfilesize > 1024*100) // rotate every 100k
    {
        setFilename(pirfilename, sizeof(pirfilename), timestamp, "pir");
    }

    pirfilesize = appendToFile(pirfilename, line);
}

void button()
{
    double timestamp = getTimestamp();
    int d = !digitalRead(BUTTONPIN) && btnfilesize;

    char line[32];
    setLine(line, sizeof(line), timestamp, d);

    if (btnfilesize == 0
    ||  btnfilesize > 1024*100) // rotate every 100k
    {
        setFilename(btnfilename, sizeof(btnfilename), timestamp, "btn");
    }

    btnfilesize = appendToFile(btnfilename, line);

    char buffer[32]={0};
    snprintf(buffer, sizeof(buffer), "BUTTON%d", d);
    system("/home/pi/sleepangel/stopring.sh");
}

int main(int argc, char *argv[])
{
    // Must be called as root
    wiringPiSetup();
    pinMode (PIRPIN, INPUT);
    pinMode (BUTTONPIN, INPUT);
    wiringPiISR (PIRPIN, INT_EDGE_BOTH, &mouvement);
    wiringPiISR (BUTTONPIN, INT_EDGE_BOTH, &button);

    // change user
    struct passwd pwd;
    struct passwd *result;
    char *buf;
    size_t bufsize;
    bufsize = sysconf(_SC_GETPW_R_SIZE_MAX);
    buf = malloc(bufsize);
    int s = getpwnam_r(USER, &pwd, buf, bufsize, &result);
    if (result == NULL)
    {
        fprintf(stderr,"Error: user \"%s\" is not found\n", USER);
        exit(1);
    }
    else
    {
        debug_print("User %s uid is %ld\n", USER, pwd.pw_uid);
    }

    if(setgid(pwd.pw_gid) != 0 || setuid(pwd.pw_uid) != 0)
    {
        fprintf(stderr,"Error: can't changer process to user \"%s\"", USER);
        exit(1);
    }

    // Create data directory if don't exist
    struct passwd *pw = getpwuid(getuid());
    const char *homedir = pw->pw_dir;
    char dir[PATH_MAX];
    snprintf(dir, PATH_MAX, "%s%s", homedir, PATH);
    struct stat sb;
    debug_print("Looking for %s\n", dir);
    if (stat(dir, &sb) != 0 || !S_ISDIR(sb.st_mode))
    {
            debug_print("Create %s\n", dir);
            mkdir(dir, 0755);
    }

    // get Timezone offset in seconds
    time_t t = time(NULL);
    struct tm lt = {0};
    localtime_r(&t, &lt);
    tzoffset = lt.tm_gmtoff; // in seconds

    mouvement();
    button();

    while(1)
    {
        sleep(1000);
    }
    return 0;
}
