//封面上传,截图

//上传后返回的文件名

var filename;

var fileid;

//裁剪主要用到了jcrop_api

var jcrop_api, boundx, boundy;

//原始文件名称

var originalfilename;

//实际图片的宽高

var imgweight, imgheight;

//dx：实际图片宽/显示宽度

//dy: 实际图片高/显示高度

//scale:最终缩放比

//  var dx,dy,scale = 1;

//  var displayW = 175, displayH = 350;

var imgObj = new Image();


$(function () {

    init();

});


function init() {

    //文件上传的js组件(FileUpload的js组件)

    $('#uploadCover').fileupload({

        dataType: 'json',

        //autoUpload: true,

        url: '/contentAffix/upTemp',


        done: function (e, data) {

            if (jcrop_api != null) {

                jcrop_api.destroy();

            }

            $.each(data.result, function (index, file) {

                if (index == 'filedesc') {

                    //获取文件名称

                    filename = file.filename;

                    //实际的文件高度

                    imgweight = file.imgweight;

                    //实际的文件宽度

                    imgheight = file.imgheight;


//                     //设置缩放比例

//                     dx = imgweight / displayW;

//                     dy = imgheight / displayH;

//                     if(dx > dy && dy > 1) {

//                         scale = dx;

//                        

//                     }

//                     if(dy > dx && dx > 1) {

//                         scale = dy;

//                     }

//                    

//                     displayW = imgweight / scale;

//                     displayH = imgheight / scale;


//                     $("#jcrop_target").css({

//                        width:displayW + 'px',

//                        height:displayH + 'px'

//                     });

//                     $(".tailoringc .tailoringl").css({

//                        width:(displayW + 2) + 'px',

//                        height:(displayH + 2) + 'px'

//                     });


                    originalfilename = file.originalfilename;

                    fileid = file.id;

                    $('#light').show();

                    $('#fade').show();


                    var imgurl = file.filepath + '/' + file.filename;

                    $('#jcrop_target').attr('src', imgurl);

                    $('#cutImgId').attr('src', imgurl);


                    cutPic();

                    //重新加载图像到jcrop，才能小图上正确显示截图位置

                    //jcrop_api.setImage(imgurl);

                }

            });

        },

    });

    $("#pickCover").click(function () {

        $("#uploadCover").trigger('click');

    });


    $('body').data('filelist', new Array());

}


//点击裁剪时做的操作

//传递到后台的是最终在实际图片上的位置和宽高

function saveUploadImg() {

    c = jcrop_api.tellSelect();

    if (parseInt(c.w) > 0) {

        $.ajax({

            url: '/cartoon-web/contentAffix/cutimageAndSaveAffix',

            data: {
                "pointx": Math.round(c.x * imgweight / 280),
                "pointy": Math.round(c.y * imgheight / 350),
                "pointw": Math.round(c.w * imgweight / 280),
                "pointh": Math.round(c.h * imgheight / 350),
                "filename": filename,
                "fileid": fileid,
                "originalfilename": originalfilename
            },

            dataType: 'json',


            success: function (data) {

                if (data.result == "success") {

                    $("#fmimg").attr('src', data.cropImgPath + "?r=" + new Date().getTime());


                    $('input[type=hidden][name=coverAffixId]').val(fileid);


                    $('#light').hide();

                    $('#fade').hide();


                    displayW = 280;

                    displayH = 350;

                } else {

                    alert("请选择图片");

                }

            }

        });

    }

}


//保存上传后的文件名称

function saveReuploadImg() {

    c = jcrop_api.tellSelect();

    var affixId = $('#coverAffixId').val();

    $.ajax({

        url: '/cartoon-web/contentAffix/cutimageAndUpdateAffix',

        data: {

            "pointx": Math.round(c.x),

            "pointy": Math.round(c.y),

            "pointw": Math.round(c.w),

            "pointh": Math.round(c.h),

            "filename": filename,

            "fileid": fileid,

            "originalfilename": originalfilename,

            "affixId": affixId

        },

        dataType: 'json',

        success: function (data) {

            if (data.result == "success") {

                $("#fmimg").attr('src', data.cropImgPath + "?r=" + new Date().getTime());

                $('input[type=hidden][name=coverAffixId]').val(fileid);

                $('#light').hide();

                $('#fade').hide();

            } else {

                alert("请选择图片");

            }

        }

    });

}


//显示预览

function showPreview(c) {

    if (parseInt(c.w) > 0) {


        var rx = 280 / c.w;

        var ry = 175 / c.h;

        var bounds = jcrop_api.getBounds();

        boundx = bounds[0];

        boundy = bounds[1];


        $('#cutImgId').css({

            width: Math.round(rx * boundx) + 'px',

            height: Math.round(ry * boundy) + 'px',

            marginLeft: '-' + Math.round(rx * c.x) + 'px',

            marginTop: '-' + Math.round(ry * c.y) + 'px',

        });

    }

}


function cutPic() {

    imgObj = new Image();

    imgObj.src = jcrop_target.src;


    jcrop_api = $.Jcrop('#jcrop_target', {

        onChange: showPreview,//选框改变时的事件

        onSelect: showPreview,//选框选定时的事件

        handleSize: 1,//缩放按钮大小

        drawBorders: false,//绘制边框

        aspectRatio: 280 / 175,//选框宽高比。说明：width/height

        allowResize: true,

        allowSelect: false, //允许新选框

        //   bgColor:"#ccc",  //背景色

//          minSize: [50,50],

//          allowMove: true,

//          allowResize:false,

//          allowSelect:true, //允许新选框

//          cornerHandles:false,  //允许边角缩放

//          sideHandles:false,  //允许四边缩放

//          handleSize:9,

//          drawBorders:true, //绘制边框

        dragEdges: true,  //允许拖动边框

//         //bgOpacity:0.9, //透明度

//           onChange:showPreview, //当选择区域变化的时候，执行对应的回调函数

//          onSelect:showPreview, //当选中区域的时候，执行对应的回调函数

//          aspectRatio:1, //正方形

        //setSelect:[300,300,300,300,0,0]

    });


    //设置选择框默认位置

    jcrop_api.animateTo([0, 0, 280, 175]);

};

