from pymvc import model, settings, router, wsgi, controller

settings.database.database = "flask_mvt_test"
app = wsgi.app


class User(model.Model):
    name = model.StringType()
    id = model.UniqueIdType(primary=True, non_null=True, unique=True)


class TestData1(model.Model):
    pass


class TestData2(model.Model):
    pass


class TestData3(model.Model):
    pass


class TestData4(model.Model):
    pass


user = User.load(primary="6f15de0e-deb0-4368-bdf1-21a87734fc14")
user.name = "new name"
user.save()


# @app.route('/')
# def hello_world():
#     return render_template("test.html")

@router.route("/")
class TopController(controller.Controller):
    VIEW = "test.html"

    def get(self, **kwargs):
        pass


# router.add_route("/", TopController)


if __name__ == '__main__':
    app.run()
