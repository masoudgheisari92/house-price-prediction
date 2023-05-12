from sklearn import tree, preprocessing

from core.models import Region, House


def predict_price(
    region: Region,
    year_of_construction: int,
    area: int,
    room: int,
) -> int:
    x = []
    y = []
    houses = House.objects.filter(region=region)
    for house in houses:
        x.append((house.year_of_construction, house.area, house.room))
        y.append(house.price)

    clf = tree.DecisionTreeClassifier()
    scaler = preprocessing.StandardScaler().fit(x)
    x_scaled = scaler.transform(x)
    clf = clf.fit(x_scaled, y)
    new_data = [(year_of_construction, area, room)]
    scaled_newdata = scaler.transform(new_data)
    price = clf.predict(scaled_newdata)
    return price[0]
