import io
from base.base_resource import BaseResource
from flask import request, send_file
from addons.image.service.image_service import ImageService
from utils.decorators import login_required


class ImageResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "image"
        self.service = ImageService

    def get_resource(self):
        '''
        return resource type image
        :return: file object
        '''
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = self.service.get_image(image_id,user_email=None, type="resource")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result

    @login_required
    def get_avatar(self):
        '''
        return avatar type image
        :return: file object
        '''
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = self.service.get_image(image_id,user_email=None, type="avatar")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result


    @login_required
    def get_bookcover(self):
        '''
        return bookcover type image
        :return: file object
        '''
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = self.service.get_image(image_id,user_email=None, type="bookcover")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result

    @login_required
    def get_upload(self):
        '''
        return seller-upload type image
        :return: file object
        '''
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = self.service.get_image(image_id, user_email=None, type="seller_upload")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result



