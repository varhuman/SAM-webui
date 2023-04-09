$(document).ready(function () {
    let points: { x: number; y: number }[] = [];
    let img = document.getElementById('clickable-image') as HTMLImageElement;
    $('#clickable-image').on('click', function (event) {
        const img = $(this);
        const offset = img.offset();

        if (offset) {
            const x = event.pageX - offset.left;
            const y = event.pageY - offset.top;
            points.push({ x: x, y: y });

            const point = $('<div class="point"></div>');
            point.css({
                left: x + 'px',
                top: y + 'px',
            });
            $('#image-container').append(point);

            console.log('Clicked at', x, y);
            console.log('Current points:', points);
        }
    });

    // Automatically submit the form when a file is selected
    $('#image').on('change', function () {
        $('#upload-form').submit();
    });

    // Show loading indicator when processing points
    $('#process-points').on('click', function () {
        $('#loading').show();
        sendPoints();
    });

    // Clear all points
    $('#clear-points').on('click', function () {
        points = [];
        $('.point').remove();
        console.log('Cleared all points');
    });

    function displayProcessedImg(imagePath: string = '') {
        const src = '/processed_image/' + imagePath;
        console.log("imagePath:", src);
        // 添加处理后的图像
        const imgElement = $('<img class="resized-image" id="output-image" src="' + src + '" alt="Output image" />');
        imgElement.css({
            "width": "100%",
            "height": "100%",
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
                displayProcessedImg(response.output_image_path);
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
