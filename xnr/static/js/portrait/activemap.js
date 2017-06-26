function month_process(data, flag){
    require.config({
        paths: {
            echarts: '/static/js/bmap/js'
        },
        packages: [
            {
                name: 'BMap',
                location: '/static/js/bmap',
                main: 'main'
            }
        ]
    });

    require(
    [
        'echarts',
        'BMap',
        'echarts/chart/map'
    ],
    function (echarts, BMapExtension) {
        // 初始化地图
        var BMapExt = new BMapExtension($('#map')[0], BMap, echarts,{
            enableMapClick: false
        });
        var map = BMapExt.getMap();
        var container = BMapExt.getEchartsContainer();
        var startPoint = {
            x: 104.114129,
            y: 37.550339
        };

        var point = new BMap.Point(startPoint.x, startPoint.y);
        map.centerAndZoom(point, 5);
        //map.enableScrollWheelZoom(true);
        //console.log(data);
        // process
        var timelist = new Array();
        var geolist = new Array();
        var addedlist = new Array();
        for (var i = 0; i < data.length; i++){
            var time_geo = data[i];
            if (time_geo[1] != ''){
                timelist.push(time_geo[0]);
                var city_city = time_geo[1].split('\t').pop();
                geolist.push(city_city);
                addedlist[city_city] = '';
            }
        }
        // marker
        var newgeo = new Array();
        var myGeo = new BMap.Geocoder();
        //var geolist = ['北京', '上海','广州','南宁', '南昌', '大连','拉萨'];
        var index = 0;
        bdGEO();
        function bdGEO(){
            var geoname = geolist[index];
            var timename = timelist[index];
            geocodeSearch(geoname, timename);
            index++;
        }
        function geocodeSearch(geoname, timename){
            if(index < geolist.length-1){
                setTimeout(bdGEO,400);
            }
            else{
                setTimeout(drawline, 400);
            }
            myGeo.getPoint(geoname, function(point){
                if (point){
                    var fixpoint= new BMap.Point(point.lng,point.lat);
                    var marker = new BMap.Marker(fixpoint);
                    addedlist[geoname] = addedlist[geoname] + ',' + timename;
                    marker.setTitle(geoname+addedlist[geoname]);
                    marker.setOffset(new BMap.Size(2,10));
                    map.addOverlay(marker);
                    newgeo[geoname] = [fixpoint.lng,fixpoint.lat];
                }
                else{
                    //alert("no such point!");
                }
            }, geoname);
        }
        function drawline(){
            var linklist = new Array();
            if (flag == true){
                var last_geo = geolist[0];
                for (var i = 1; i < geolist.length; i++){
                    linklist.push([{name:last_geo},{name:geolist[i], value:90}]);
                    last_geo = geolist[i];
                }
            }
            else{
            }
            //console.log(linklist);
            //linklist = [[{name:'北京'}, {name:'南宁',value:90}],[{name:'北京'}, {name:'南昌',value:90}],[{name:'北京'}, {name:'拉萨',value:90}]];
            //console.log(linklist);
            var option = {
                color: ['gold','aqua','lime'],
                title : {
                    text: '',
                    subtext:'',
                    x:'center',
                    textStyle : {
                        color: '#fff'
                    }
                },
                tooltip : {
                    trigger: 'item',
                    formatter: function (v) {
                        return v[1].replace(':', ' > ');
                    }
                },
                toolbox: {
                    show : false,
                    orient : 'vertical',
                    x: 'right',
                    y: 'center',
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                dataRange: {
                    show: false,
                    min : 0,
                    max : 100,
                    range: {
                        start: 10,
                        end: 90
                    },
                    x: 'right',
                    calculable : true,
                    color: ['#ff3333', 'orange', 'yellow','lime','aqua'],
                    textStyle:{
                        color:'#fff'
                    }
                },
                series : [
                    {
                        name:'全国',
                        type:'map',
                        mapType: 'none',
                        data:[],
                        geoCoord: newgeo,
                        markLine : {
                            smooth:true,
                            effect : {
                                show: true,
                                scaleSize: 1,
                                period: 30,
                                color: '#fff',
                                shadowBlur: 10
                            },
                            itemStyle : {
                                normal: {
                                    borderWidth:1,
                                    label:{show:false},
                                    lineStyle: {
                                        type: 'solid',
                                        shadowBlur: 10
                                    }
                                }
                            },
                            data : linklist
                        },
                    }
                ]
            };

            var myChart = BMapExt.initECharts(container);
            window.onresize = myChart.onresize;
            BMapExt.setOption(option);
        }
    }
);
}

function location_all(){
    var location_geo;
    // location table
    $('#total_location_rank').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th>';
    for (var i = 0; i < 5; i++){
        var s = i.toString();
        var m = i + 1;
        html += '<th style="text-align:center">' + m + '</th>';
    }
    html += '<th style="text-align:center;"></th>';
    html += '</tr>';

    var url = '/attribute/location/?uid='+uid+'&time_type=day';
    var daily_location_map_data = new Array();
    activity_call_ajax_request(url, location_day);
    function location_day(data){
        //day
        //console.log(data);
        var tag_vector = data.tag_vector;
        global_tag_vector.push(tag_vector);

        location_geo = data.sort_results;
        html += '<tr><th style="text-align:center">当日</th>';
        for (var i = 0; i < location_geo.length; i++) {
            daily_location_map_data.push(['top'+(i+1), location_geo[i][0]]);
            html += '<th style="text-align:center">' + location_geo[i][0] + '(' + location_geo[i][1] + ')</th>';
        }
        while (i < 5){
            html += '<th style="text-align:center">-</th>';
            i++;
        }
        html += '<th style="text-align:center"><a id="daily_location_map" href="#map">查看地图</a></th>';
        html += '</tr>';
    }
    var url = '/attribute/location/?uid='+uid+'&time_type=week';
    var weekly_location_map_data = new Array();
    activity_call_ajax_request(url, location_week);
    function location_week(data){
        //week
        location_geo = data.week_top;
        html += '<tr><th style="text-align:center">最近7天</th>';
        for (var i = 0; i < location_geo.length; i++) {
            weekly_location_map_data.push(['top'+(i+1), location_geo[i][0]]);
            html += '<th style="text-align:center">' + location_geo[i][0] + '(' + location_geo[i][1] + ')</th>';
        }
        while (i < 5){
            html += '<th style="text-align:center">-</th>';
            i++;
        }
        html += '<th style="text-align:center"><a id="weekly_location_map" href="#map">查看地图</a></th>';
    }
    var url = '/attribute/location/?uid='+uid+'&time_type=month';
    var monthly_location_map_data = new Array();
    activity_call_ajax_request(url, location_month);
    function location_month(data){
        //console.log(data);
        $('#locate_desc').html("<span style='color:red;'>" + data.description[0] + "</span><span>" + data.description[1] + "</span>。"); //description
        //month
        location_geo = data.all_top;
        html += '<tr><th style="text-align:center">最近30天</th>';
        for (var i = 0; i < location_geo.length; i++) {
            monthly_location_map_data.push(['top'+(i+1), location_geo[i][0]]);
            html += '<th style="text-align:center">' + location_geo[i][0] + '(' + location_geo[i][1] + ')</th>';
        }
        while (i < 5){
            html += '<th style="text-align:center">-</th>';
            i++;
        }
        html += '<th style="text-align:center"><a id="monthly_location_map" href="#map">查看地图</a></th>';
        html += '</tr>';
        // track map
        // month_process(data.month_track, true);
        bind_map();
        function bind_map(){
            $('#month_track').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block')
                month_process(data.month_track, true);
            });

            $('#more_track').click(function(){
                var div0 = document.getElementById('active_geo');
                var div1 = document.getElementById('more_t_list');
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+130+'px';
                }                
                $('#more_t_list').css('display', 'block');
                //month_process(data.month_track, true);
            });

            $('#total_daily_ip_map').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block');
                month_process(daily_map_data, false);
            });
            $('#total_weekly_ip_map').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block');
                month_process(weekly_map_data, false);
            });
            $('#span_daily_ip_map').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block');
                month_process(span_daily_map_data, true);
            });
            $('#span_weekly_ip_map').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block');
                month_process(span_weekly_map_data, true);
            });
        }
    }
    html += '</table>'; 
    $('#total_location_rank').append(html);
    bind_location_map();
    function bind_location_map(){
        $('#daily_location_map').click(function(){
		var div0 = document.getElementById('active_geo');  
		var div1 = document.getElementById('map');                
		if(div1.style.display=='none'){
		div0.style.height=div0.offsetHeight+850+'px';
		}
	$('#map').css('display', 'block');
            month_process(daily_location_map_data, false);
        });
        $('#weekly_location_map').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block');
            month_process(weekly_location_map_data, false);
        });
        $('#monthly_location_map').click(function(){
                var div0 = document.getElementById('active_geo');  
                var div1 = document.getElementById('map');                
                if(div1.style.display=='none'){
                 div0.style.height=div0.offsetHeight+850+'px';
                }
                $('#map').css('display', 'block');
            month_process(monthly_location_map_data, false);
        });
    }

}
location_all();

