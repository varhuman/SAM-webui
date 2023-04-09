$(document).ready(function () {
    let points: { x: number; y: number }[] = [];
    let img = document.getElementById('clickable-image') as HTMLImageElement;
    $('#clickable-image').on('click', function (event) {
        const img = $(this);
    
        const x = event.offsetX;
        const y = event.offsetY;
    
        // 确保点击点在图片范围内
        if (x < 0 || x > img.width()! || y < 0 || y > img.height()!) {
            return;
        }
    
        points.push({ x: x, y: y });
    
        const point = $('<div class="point"></div>');
        point.css({
            left: x + 'px',
            top: y + 'px',
        });
        $('#image-container').append(point);
    
        console.log('Clicked at', x, y);
        console.log('Current points:', points);
    });    

    // Automatically submit the form when a file is selected
    $('#image').on('change', function () {
        $('#upload-form').submit();
    });

    $("#process-points").on("click", function () {
        const points = getPoints();
        if (points.length === 0) {
          $("#no-points-warning").show();
          return;
        } else {
          $("#no-points-warning").hide();
        }
        $('#loading').show();
        sendPoints();
    });

    // Clear all points
    $('#clear-points').on('click', function () {
        points = [];
        $('.point').remove();
        console.log('Cleared all points');
    });

    function getPoints() {
        return points;
      }

    function displayProcessedImg(imagePath: string = '', originalWidth: number, originalHeight: number) {
        const randomParam = '?rand=' + Math.random();
        const src = '/processed_image/' + imagePath + randomParam;
        console.log("imagePath:", src);
    
        // 计算处理后的图像的宽度和高度，以保持宽高比
        const containerWidth = $('#output-image-container').width()!;
        const containerHeight = $('#output-image-container').height()!;
        const aspectRatio = originalWidth / originalHeight;
        let width, height;
    
        if (containerWidth / containerHeight > aspectRatio) {
            width = containerHeight * aspectRatio;
            height = containerHeight;
        } else {
            width = containerWidth;
            height = containerWidth / aspectRatio;
        }
    
        // 添加处理后的图像
        const imgElement = $('<img class="resized-image" id="output-image" src="' + src + '" alt="Output image" />');
        imgElement.css({
            "width": width,
            "height": height,
            "object-fit": "contain",
        });
        $('#output-image-container').empty().append(imgElement);
    }

    function getDisplayedImageSize(image: HTMLImageElement) {
        return {
            width: image.clientWidth,
            height: image.clientHeight,
        };
    }

    // 修改 sendPoints 函数以处理服务器响应
    function sendPoints() {
        console.log('Request data:', {
            points: points,
            img_size: getDisplayedImageSize(img),
        });

        $.ajax({
            type: 'POST',
            url: '/process_points',
            contentType: 'application/json',
            data: JSON.stringify({
                points: points,
                img_size: getDisplayedImageSize(img),
            }),
            success: function (response) {
                console.log('Points sent to server:', response);
                displayProcessedImg(response.output_image_path, img.naturalWidth, img.naturalHeight);
                $('#loading').hide();
                $('#download-mask').show().attr('data-mask-url', response.mask_image_path);
            },
            error: function (error) {
                console.error('Error sending points:', error);
                $('#loading').hide();
            },
        });
    }

    function downloadMask(url: string) {
        $('#download-mask').attr('href', url);
    }

    $('#download-mask').on('click', function () {
        const maskUrl = $(this).attr('data-mask-url') ?? '';
        console.log('Variable value:', maskUrl);
        downloadMask(maskUrl);
    });
});
