# DRF MDO
Опыты с DRF .

Деплои стандартный:
git pull , pip install -r requements.txt , ./manage.py migrate ./manage.py makemigrations , ./manage.py migrate ./manage.py createsuperuser , дальше в админку добавлять данные и пользователей. Потом можно [поиграться с постманом](https://github.com/saintbyte/drf_mdo/blob/master/Entity_Test.postman_collection.json)

  Поставлены такие задачи:

> 1. Как правильно сохранять modified_by?
> Пояснение: при создании записи в запросе приходит только value, но в
> БД нужно записать не только value, но и того пользователя, который
> сделал POST-запрос.
> Подсказка: Модели и сериализатор остаются неизменными

Если нельзя править модель сериализатор - то остается view.
Для этого:

    permission_classes = [IsAuthenticated,]

Чтобы пользователь был всегда. Потом добавим во View метод [perform_create](https://github.com/saintbyte/drf_mdo/blob/86834fb8e8b4c666c96f4a828c0af4810ec637d3/drf_entity/entity/api_views.py#L22)


> 2. Для создания Entity на вход POST API подаётся json вида
>      {"data[value]": 10}
> Как исправить сериализатор так, чтобы он мог принять поле
> "data[value]" и сохранить его в поле value?
> Пояснение: Python не позволит написать в сериализаторе `data[value] =
> IntegerField(...)`, но есть другое решение Подсказка: Модели остаются
> неизменными

Проблема в то что json на входе вполне валидный, самое очевидное что приходит в голову `value = IntegerField(source="data[value]")`
Оно тоже как бы валидно со всех сторон , но не работает. Крайне странный случай вообще. get_value, validate_value тоже не дают результата. Единственное что приходит на ум (и гарантировано рабочие) патчить Request во View. В метод create во view передается request типа [Request из DRF](https://github.com/encode/django-rest-framework/blob/master/rest_framework/request.py) и там data есть, но только для чтения. И приходится использовать относительно грязный хак что переопределить data в переменной. Есть еще [такой хак](https://www.valentinog.com/blog/drf-request/) с сериализером но там больше кода. [Реализация в гитхабе](https://github.com/saintbyte/drf_mdo/blob/86834fb8e8b4c666c96f4a828c0af4810ec637d3/drf_entity/entity/api_views.py#L25)


> 3. Как вывести properties в формате {key:value, ...}, если мы заранее не знаем сколько и каких key может быть?
>
> Пояснение: Иногда нужно вывести данные, когда имена полей заранее
> неизвестны. См. пример ниже. Не обращайте внимания на то, что value -
> строка, это всего лишь пример, как может выглядеть properties.
>
>
>
>     [
>        {
>           "value":"circle",
>           "properties":{
>              "center":"100, 100",
>              "radius":"50"
>           }
>        },
>        {
>           "value":"line",
>           "properties":{
>              "start":"150, 50",
>              "end":"50, 150"
>           }
>        },
>        {
>           "value":"Медведь",
>           "properties":{
>              "класс":"Млекопитающие"
>           }
>        },
>        {
>           "value":"rectangle",
>           "properties":{
>              "corner_1":"50, 50",
>              "corner_2":"150, 150"
>           }
>        }
>     ]
>
> Есть много способов решить эту задачу, нужно выбрать максимально
> правильный способ

Постановка вопроса про правильность сама по себе некорректна, а это еще и питон в котором существует 10 способов решить одну и туже задачу. По мне  самый простой способ в 5 строк это использовать SerializerMethodField для properties. Можно еще короче написать метод но будет менее читаемый =)

[Код в гитхабе](https://github.com/saintbyte/drf_mdo/blob/86834fb8e8b4c666c96f4a828c0af4810ec637d3/drf_entity/entity/serializers.py#L13)


    def  get_properties(self, obj):
      result_dict = {}
      for  prop  in  obj.properties.all():
           result_dict[prop.key] = prop.value
      return  result_dict
