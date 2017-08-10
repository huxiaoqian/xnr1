// public_ajax.call_request('get',weibo_url,weibo);
function weibo(data){
    $('#group_emotion_loading').css('display', 'none');
    // $('#input-table').css('display', 'block');
    var dataArray = window.JSON?JSON.parse(data):eval("("+data+")");;
    var PageNo=document.getElementById('PageNo');                   //设置每页显示行数
    var InTb=document.getElementById('input-table');               //表格
    var Fp=document.getElementById('F-page');                      //首页
    var Nep=document.getElementById('Nex-page');                  //下一页
    var Prp=document.getElementById('Pre-page');                  //上一页
    var Lp=document.getElementById('L-page');                     //尾页
    var S1=document.getElementById('s1');                         //总页数
    var S2=document.getElementById('s2');                         //当前页数
    var currentPage;                                              //定义变量表示当前页数
    var SumPage;

    if(PageNo.value!="")                                       //判断每页显示是否为空
    {
        InTb.innerHTML='';                                     //每次进来都清空表格
        S2.innerHTML='';                                        //每次进来清空当前页数
        currentPage=1;                                          //首页为1
        S2.appendChild(document.createTextNode(currentPage));
        S1.innerHTML='';                                        //每次进来清空总页数
        if(dataArray.length%PageNo.value==0)                    //判断总的页数
        {
            SumPage=parseInt(dataArray.length/PageNo.value);
        }
        else
        {
            SumPage=parseInt(dataArray.length/PageNo.value)+1
        }
        S1.appendChild(document.createTextNode(SumPage));
        var oTBody=document.createElement('tbody');               //创建tbody
        oTBody.setAttribute('class','In-table');                   //定义class
        InTb.appendChild(oTBody);                                     //将创建的tbody添加入table
        var html_c = '';

        if(dataArray==''){
            html_c = "<p style='text-align: center'>用户未发布任何微博</p>";
            oTBody.innerHTML = html_c;
        }else{

            for(i=0;i<parseInt(PageNo.value);i++)
            {                                                          //循环打印数组值
                oTBody.insertRow(i);
                var text,time;
                if (dataArray[i].time==''||dataArray[i].time=='unknown') {
                    time='未知';
                }else {
                    time=dataArray[i].time;
                };
                if (dataArray[i].text==''||dataArray[i].text=='unknown') {
                    text='未发表任何内容';
                }else {
                    text=dataArray[i].text;
                };
                html_c =
                    '<div class="published">'+
                    '     <span id="'+dataArray[i].mid+'"></span>'+
                    '     <p class="master">'+
                    '          微博内容：'+
                    '          <span class="master1">'+text+'</span>'+
                    '     </p>'+
                    '     <p class="time">'+
                    '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
                    '        <span style="display: inline-block;float:right;">'+
                    '        <span class="time4">转发数（'+dataArray[i].retweeted+'）</span>|&nbsp;'+
                    '        <span class="time5">评论数（'+dataArray[i].comment+'）</span></span>'+
                    '     </p>'+
                    '</div>';
                oTBody.rows[i].insertCell(0);
                oTBody.rows[i].cells[0].innerHTML = html_c;
            }
        }
    }

    Fp.onclick=function()
    {

        if(PageNo.value!="")                                       //判断每页显示是否为空
        {
            InTb.innerHTML='';                                     //每次进来都清空表格
            S2.innerHTML='';                                        //每次进来清空当前页数
            currentPage=1;                                          //首页为1
            S2.appendChild(document.createTextNode(currentPage));
            S1.innerHTML='';                                        //每次进来清空总页数
            if(dataArray.length%PageNo.value==0)                    //判断总的页数
            {
                SumPage=parseInt(dataArray.length/PageNo.value);
            }
            else
            {
                SumPage=parseInt(dataArray.length/PageNo.value)+1
            }
            S1.appendChild(document.createTextNode(SumPage));
            var oTBody=document.createElement('tbody');               //创建tbody
            oTBody.setAttribute('class','In-table');                   //定义class
            InTb.appendChild(oTBody);                                     //将创建的tbody添加入table
            var html_c = '';

            if(dataArray==''){
                html_c = "<p style='width:840px;text-align: center'>用户未发布任何微博</p>";
                oTBody.innerHTML = html_c;
            }else{

                for(i=0;i<parseInt(PageNo.value);i++)
                {                                                          //循环打印数组值
                    oTBody.insertRow(i);
                    var text,time;
                    if (dataArray[i].time==''||dataArray[i].time=='unknown') {
                        time='未知';
                    }else {
                        time=dataArray[i].time;
                    };
                    if (dataArray[i].text==''||dataArray[i].text=='unknown') {
                        text='未发表任何内容';
                    }else {
                        text=dataArray[i].text;
                    };
                    html_c =
                        '<div class="published">'+
                        '     <span id="'+dataArray[i].mid+'"></span>'+
                        '     <p class="master">'+
                        '          微博内容：'+
                        '          <span class="master1">'+text+'</span>'+
                        '     </p>'+
                        '     <p class="time">'+
                        '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
                        '        <span style="display: inline-block;float:right;">'+
                        '        <span class="time4">转发数（'+dataArray[i].retweeted+'）</span>|&nbsp;'+
                        '        <span class="time5">评论数（'+dataArray[i].comment+'）</span></span>'+
                        '     </p>'+
                        '</div>';
                    oTBody.rows[i].insertCell(0);
                    oTBody.rows[i].cells[0].innerHTML = html_c;
                }
            }
        }
    }

    Nep.onclick=function()
    {
        if(currentPage<SumPage)                                 //判断当前页数小于总页数
        {
            InTb.innerHTML='';
            S1.innerHTML='';
            if(dataArray.length%PageNo.value==0)
            {
                SumPage=parseInt(dataArray.length/PageNo.value);
            }
            else
            {
                SumPage=parseInt(dataArray.length/PageNo.value)+1
            }
            S1.appendChild(document.createTextNode(SumPage));
            S2.innerHTML='';
            currentPage=currentPage+1;
            S2.appendChild(document.createTextNode(currentPage));
            var oTBody=document.createElement('tbody');
            oTBody.setAttribute('class','In-table');
            InTb.appendChild(oTBody);
            var a;                                                 //定义变量a
            a=PageNo.value*(currentPage-1);                       //a等于每页显示的行数乘以上一页数
            var c;                                                  //定义变量c
            if(dataArray.length-a>=PageNo.value)                  //判断下一页数组数据是否小于每页显示行数
            {
                c=PageNo.value;
            }
            else
            {
                c=dataArray.length-a;
            }
            for(i=0;i<c;i++)
            {
                oTBody.insertRow(i);
                var text,time;
                if (dataArray[i+a].time==''||dataArray[i+a].time=='unknown') {
                    time='未知';
                }else {
                    time=dataArray[i+a].time;
                };
                if (dataArray[i+a].text==''||dataArray[i+a].text=='unknown') {
                    text='未发表任何内容';
                }else {
                    text=dataArray[i+a].text;
                };
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="published">'+
                    '     <span id="'+dataArray[i+a].mid+'"></span>'+
                    '     <p class="master">'+
                    '          微博内容：'+
                    '          <span class="master1">'+text+'</span>'+
                    '     </p>'+
                    '     <p class="time">'+
                    '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
                    '        <span style="display: inline-block;float:right;">'+
                    '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                    '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                    '     </p>'+
                    '</div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
                //数组从第i+a开始取值
            }
        }
    }

    Prp.onclick=function()
    {
        if(currentPage>1)                        //判断当前是否在第一页
        {
            InTb.innerHTML='';
            S1.innerHTML='';
            if(dataArray.length%PageNo.value==0)
            {
                SumPage=parseInt(dataArray.length/PageNo.value);
            }
            else
            {
                SumPage=parseInt(dataArray.length/PageNo.value)+1
            }
            S1.appendChild(document.createTextNode(SumPage));
            S2.innerHTML='';
            currentPage=currentPage-1;
            S2.appendChild(document.createTextNode(currentPage));
            var oTBody=document.createElement('tbody');
            oTBody.setAttribute('class','In-table');
            InTb.appendChild(oTBody);
            var a;
            a=PageNo.value*(currentPage-1);
            for(i=0;i<parseInt(PageNo.value);i++)
            {
                oTBody.insertRow(i);
                var text,time;
                if (dataArray[i+a].time==''||dataArray[i+a].time=='unknown') {
                    time='未知';
                }else {
                    time=dataArray[i+a].time;
                };
                if (dataArray[i+a].text==''||dataArray[i+a].text=='unknown') {
                    text='未发表任何内容';
                }else {
                    text=dataArray[i+a].text;
                };
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="published">'+
                    '     <span id="'+dataArray[i+a].mid+'"></span>'+
                    '     <p class="master">'+
                    '          微博内容：'+
                    '          <span class="master1">'+text+'</span>'+
                    '     </p>'+
                    '     <p class="time">'+
                    '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
                    '        <span style="display: inline-block;float:right;">'+
                    '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                    '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                    '     </p>'+
                    '</div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
            }
        }
    }

    Lp.onclick=function()
    {
        InTb.innerHTML='';
        S1.innerHTML='';
        if(dataArray.length%PageNo.value==0)
        {
            SumPage=parseInt(dataArray.length/PageNo.value);
        }
        else
        {
            SumPage=parseInt(dataArray.length/PageNo.value)+1
        }
        S1.appendChild(document.createTextNode(SumPage));
        S2.innerHTML='';
        currentPage=SumPage;
        S2.appendChild(document.createTextNode(currentPage));
        var oTBody=document.createElement('tbody');
        oTBody.setAttribute('class','In-table');
        InTb.appendChild(oTBody);
        var a;
        a=PageNo.value*(currentPage-1);
        var c;
        if(dataArray.length-a>=PageNo.value)
        {
            c=PageNo.value;
        }
        else
        {
            c=dataArray.length-a;
        }
        for(i=0;i<c;i++)
        {
            oTBody.insertRow(i);
            var text,time;
            if (dataArray[i+a].time==''||dataArray[i+a].time=='unknown') {
                time='未知';
            }else {
                time=dataArray[i+a].time;
            };
            if (dataArray[i+a].text==''||dataArray[i+a].text=='unknown') {
                text='未发表任何内容';
            }else {
                text=dataArray[i+a].text;
            };
            oTBody.rows[i].insertCell(0);
            html_c =
                '<div class="published">'+
                '     <span id="'+dataArray[i+a].mid+'"></span>'+
                '     <p class="master">'+
                '          微博内容：'+
                '          <span class="master1">'+text+'</span>'+
                '     </p>'+
                '     <p class="time">'+
                '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
                '        <span style="display: inline-block;float:right;">'+
                '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                '     </p>'+
                '</div>';
            oTBody.rows[i].cells[0].innerHTML = html_c;
        }
    }

}
weibo();
