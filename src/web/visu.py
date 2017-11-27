#!/usr/bin/python

import cherrypy
import os, glob
from os import listdir
from os.path import isfile, join
import calendar, datetime, time

datadir = '/root/data/'

class SleepVisu(object):

    def is_number(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @cherrypy.expose
    def index(self):
        return """<html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Sleep angel</title>
            <link rel="stylesheet" media="all" type="text/css" href="/static/style.css" />
            <link rel="stylesheet" media="all" type="text/css" href="/static/jquery-ui.min.css" />
            <link rel="stylesheet" media="all" type="text/css" href="/static/jquery-ui-timepicker-addon.css" />

            <script language="javascript" type="text/javascript" src="/static/jquery.js"></script>
            <script language="javascript" type="text/javascript" src="/static/jquery-ui.js"></script>
            <script language="javascript" type="text/javascript" src="/static/jquery-ui-sliderAccess.js"></script>
            
            <script language="javascript" type="text/javascript" src="/static/jquery.flot.js"></script>
            <script language="javascript" type="text/javascript" src="/static/jquery.flot.time.js"></script>

            <script language="javascript" type="text/javascript" src="/static/jquery-ui-timepicker-addon.js"></script>

            <script type="text/javascript">
            $(function()
            {
                
                var startDateTextBox = $('#date_start');
                var endDateTextBox = $('#date_end');

                $.timepicker.datetimeRange(
                startDateTextBox,
                endDateTextBox,
                {
                    minInterval: (1000*60), // 1min
                    dateFormat: 'dd/mm/yy', 
                    timeFormat: 'HH:mm',
                    start: {
                            addSliderAccess: true,
                            sliderAccessArgs: { touchonly: false }
                            },
                    end: {
                            addSliderAccess: true,
                            sliderAccessArgs: { touchonly: false }
                    }
                }
                );

                var today = new Date();
                today.setHours(8);
                today.setMinutes(0);
            
                var yday = new Date();
                yday.setDate(yday.getDate() - 1);
                yday.setHours(22);
                yday.setMinutes(0);

                startDateTextBox.datetimepicker('setDate', yday);
                endDateTextBox.datetimepicker('setDate', today);

                 var autopool = true;

                $("button.dataSel").click(function ()
                {
                    autopool = false;

                    var startDate = startDateTextBox.datetimepicker('getDate');
                    var endDate = endDateTextBox.datetimepicker('getDate');

                    if (startDate.getTime() > endDate.getTime())
                    {
                        alert("The start must be before the end !");
                        return;
                    }

                    var data = [];

                    var options = {
                        lines: {
                            show: true,
                            fill: true,
                            steps: true
                        },
                        xaxis: {
                            mode: "time" 
                        },
                        yaxis : {
                            ticks: [[0, "inactif"], [1, "mouvement"]],
                            min: -0.25,
                            max: 1.5
                        }
                    };

                    $.plot("#placeholder", data, options);

                    var dataurl = 'datarange?s='+startDate.getTime()+'&e='+endDate.getTime();

                    function onDataReceived(series) {
                            data = [ series.pir,series.btn ];
                            $.plot("#placeholder", data, options);
                            $("#tcumul").text(series.tcumul);
                    }

                    $.ajax({
                            url: dataurl,
                            type: "GET",
                            dataType: "json",
                            success: onDataReceived
                    });

                });


                $("button.dataLive").click(function ()
                {
                    autopool = true;

                    var data = [];

                    var options = {
                        lines: {
                            show: true,
                            fill: true,
                            steps: true
                        },
                        xaxis: {
                            mode: "time" 
                        },
                        yaxis : {
                            ticks: [[0, "inactif"], [1, "mouvement"]],
                            min: -0.25,
                            max: 1.5
                        }
                    };

                    $.plot("#placeholder", data, options);

                    function fetchData() {

                        var dataurl = "data";

                        function onDataReceived(series) {
                            if (autopool)
                            {
                                data = [ series.pir,series.btn ];
                                $.plot("#placeholder", data, options);
                                $("#tcumul").text(series.tcumul);
                            }
                        }

                        $.ajax({
                            url: dataurl,
                            type: "GET",
                            dataType: "json",
                            success: onDataReceived
                        });

                        if (autopool)
                        {
                            setTimeout(fetchData, 1000);
                        }
                    }

                    setTimeout(fetchData, 1000);
                });

                $("button.dataLive").click();
            });

            </script>
        </head>
    <body>
    <div id="header">
        <h2>Moniteur</h2>
    </div>

    <div id="content">

        <div class="sleep-container">
            <div id="placeholder" class="sleep-placeholder"></div>
        </div>

        <p>
            <input type="text" class="datetime" id="date_start"> to 
            <input type="text" class="datetime" id="date_end">
            <button class="dataSel">Selectionner</button>
            <button class="dataLive">Direct</button>
        </p>
       <div>
       Temps cumul&eacute; des mouvements: <span id="tcumul">en cours de calcul</span>
       </div>
       </div>
    </div>
    </body>
</html>"""

    def getLastData(self,extension):
        data = []
        os.chdir(datadir)
        files = [ f for f in glob.glob('*.'+extension)]
        lastfile = sorted(files)[-1]
        with open(lastfile) as f: content = f.readlines()
        for i in content:
            try:
                t = i.split(',')
                vtime = int(t[0])
                state = int(t[1].rstrip())
                data.append([vtime,state])
            except:
                pass
        data.append([calendar.timegm(datetime.datetime.now().timetuple())*1000,0])
        return data

    def getCumulSince(self,extension,minutes):
        data= []
        os.chdir(datadir)
        files = [ f for f in glob.glob('*.'+extension)]
        lastfile = sorted(files)[-1]
        with open(lastfile) as f: content = f.readlines()
        for i in content:
            try:
                t = i.split(',')
                vtime = int(t[0])
                state = int(t[1].rstrip())
                now = calendar.timegm(datetime.datetime.now().timetuple())*1000
                timelimit = now - (minutes*60*1000)
                if vtime > timelimit:
                    data.append([vtime,state])
            except:
                pass
        cumul = self.getCumul(data)
        return cumul

    def getCumul(self,data):
        tcumul=0
        last1=0
        for t,v in data:
            if v == 1:
               last1 = t
            else:
                if last1 != 0:
                    tcumul = tcumul + (t-last1)
                    last1=0
        return tcumul

    @cherrypy.expose
    def last10(self):
        cumul = self.getCumulSince('pir',10)
        return str(cumul)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def data(self):

        pir = self.getLastData('pir')
        btn = self.getLastData('btn')
        tcumul = self.getCumul(pir)

        return { "tcumul": tcumul, "pir" : {"label" : "mouvements", "data": pir}, "btn" : {"label" : "button", "data": btn } }

    def getDataFromRange(self,s,e,extension):
        data = [[s,0]]
        
        files = [ f for f in glob.glob('*.'+extension)]
        sorted_files = sorted(files)
        first_file = int(sorted_files[0].split('.')[0])
        last_file = int(sorted_files[-1].split('.')[0])
        for fn in sorted_files:
            tm = int(fn.split('.')[0])
            if tm <= s:
                first_file = tm
            if tm <= e:
                last_file = tm
            else:
                break
        
        selected_files=[]
        for fn in sorted_files:
            tm = int(fn.split('.')[0])
            if tm >= first_file and tm <= last_file:
                selected_files.append(str(tm)+'.'+extension)

        for fn in selected_files:
            with open(fn) as f: content = f.readlines()
            for i in content:
                try:
                    t = i.split(',')
                    vtime = int(t[0])
                    state = int(t[1].rstrip())
                    if vtime >= s and vtime <= e:
                        data.append([vtime,state])
                except:
                    pass
        data.append([e,0])
        return data


    @cherrypy.tools.json_out()
    @cherrypy.expose
    def datarange(self, s=0, e=0):
        os.chdir(datadir)

        tzoffset = calendar.timegm(datetime.datetime.now().timetuple()) - time.time()

        s = int(int(s) + tzoffset*1000)
        e = int(int(e) + tzoffset*1000)

        pir = self.getDataFromRange(s,e,'pir')
        btn = self.getDataFromRange(s,e,'btn')
        tcumul = self.getCumul(pir)
        
        return { "tcumul": tcumul, "pir" : {"label" : "mouvements", "data": pir}, "btn" : {"label" : "button", "data": btn } }

if __name__ == '__main__':

    cherrypy.config.update(
        {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 80,
        })

    conf = {
            '/': {
                    'tools.sessions.on': True,
#                    'tools.staticdir.root': os.path.abspath(os.getcwd())
                    'tools.staticdir.root': '/home/pi/sleepangel/web/'
                },
            '/static': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': './static'
                }
            }

    cherrypy.quickstart(SleepVisu(), '/', conf)

