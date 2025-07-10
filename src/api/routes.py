"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Products, Categories, Purchases, Favorites, Ratings, Product_images
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

#Get all users
@api.route('/users', methods=['GET'])
def get_users():
    stmt =select(Users)
    users = db.session.execute(stmt).scalars().all()
    return jsonify([user.serialize() for user in users]), 200

#Get single user
@api.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    stmt = select(Users).where(Users.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({'error' : f'user with id {user_id} not found'}), 404 
    return jsonify(user.serialize()), 200

#Post user (create user)
@api.route('/users', methods=['POST'])
def create_user():
    data= request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'missing data to create an user'}), 400
    new_user = Users(
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

#Put user (modify user)
@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    stmt = select(Users).where(Users.id == id)
    user= db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({'error': f'user {id} not found'}), 404
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.name = data.get('name', user.name)
    user.surname= data.get('surname', user.surname)
    user.average_rating_as_seller=data.get('average_rating_as_seller', user.average_rating_as_seller)
    user.average_rating_as_buyer= data.get('average_rating_as_buyer', user.average_rating_as_buyer)
    user.avatar_url= data.get('avatar_url', user.avatar_url)
    db.session.commit()
    return jsonify({'data': user.serialize(), 'message': f'user with id {id} modified'}), 200

#Delete user 
@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({'error': f'user with id {id} not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'user with id {id} deleted'}), 200
    
        
#Get all products
@api.route('/products', methods=['GET'])
def get_products():
    stmt =select(Products)
    products = db.session.execute(stmt).scalars().all()
    return jsonify([product.serialize() for product in products]), 200

#Get single product
@api.route('/products/<int:product_id>', methods=['GET'])
def get_single_product(product_id):
    stmt = select(Products).where(Products.id == product_id)
    product = db.session.execute(stmt).scalar_one_or_none()
    if product is None:
        return jsonify({'error' : f'product with id {product_id} not found'}), 404 
    return jsonify(product.serialize()), 200


#Post product (create product)
@api.route('/products', methods=['POST'])
def create_product():
    data= request.get_json()
    if not data or 'title' not in data or 'price' not in data:
        return jsonify({'error': 'missing data to create a product'}), 400
    #Validate owner and category for the product
    owner = Users.query.get(data['owner_id'])
    if not owner:
        return jsonify({'error': 'owner not found'}), 404
    category = Categories.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'category not found'}), 404
    
    new_product = Products(
        title=data['title'],
        description = data.get('description'),
        price=data['price'],
        is_sold = False,
        owner_id = data['owner_id'],
        category_id = data['category_id'],
        )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize()), 201

#Put product (modify product)
@api.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    stmt = select(Products).where(Products.id == id)
    product= db.session.execute(stmt).scalar_one_or_none()
    if product is None:
        return jsonify({'error': f'product with id {id} not found'}), 404
    product.title = data.get('title', product.title)
    product.description= data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.is_sold= data.get('is_sold', product.is_sold)
    product.owner_id = data.get('owner_id', product.owner_id)
    product.category_id=data.get('category_id', product.category_id)
    product.average_rating= data.get('average_rating', product.average_rating)
    db.session.commit()
    return jsonify({'data': product.serialize(), 'message': f'product with id {id} modified'}), 200

#Delete product 
@api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    stmt = select(Products).where(Products.id == id)
    product = db.session.execute(stmt).scalar_one_or_none()
    if product is None:
        return jsonify({'error': f'product with id {id} not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': f'product with id {id} deleted'}), 200


#Get all product_images
@api.route('/product_images', methods=['GET'])
def get_product_images():
    stmt =select(Product_images)
    product_images = db.session.execute(stmt).scalars().all()
    return jsonify([product_image.serialize() for product_image in product_images]), 200

#Get single product_image
@api.route('/product_images/<int:id>', methods=['GET'])
def get_single_product_image(id):
    stmt = select(Product_images).where(Product_images.id == id)
    product_image = db.session.execute(stmt).scalar_one_or_none()
    if product_image is None:
        return jsonify({'error' : f'product_image with id {id} not found'}), 404 
    return jsonify(product_image.serialize()), 200


#Post product_image (create product_image)
@api.route('/product_images', methods=['POST'])
def create_product_image():
    data= request.get_json()
   
    if not data or 'product_id' not in data or 'image_url' not in data:
        return jsonify({'error': 'missing data to create a product_image'}), 400
    #Validate product
    product = Products.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'product_id not found'}), 404
   
    new_product_image = Product_images(
        product_id=data['product_id'],
        image_url=data['image_url'],
       
    )
    db.session.add(new_product_image)
    db.session.commit()
    return jsonify(new_product_image.serialize()), 201

#Put product_image (modify product_image)
@api.route('/product_images/<int:id>', methods=['PUT'])
def update_product_image(id):
    data = request.get_json()
    stmt = select(Product_images).where(Product_images.id == id)
    product_image= db.session.execute(stmt).scalar_one_or_none()
    if product_image is None:
        return jsonify({'error': f'product_image {id} not found'}), 404
    product_image.product_id = data.get('product_id', product_image.product_id)
    product_image.image_url = data.get('image_url', product_image.image_url)
    db.session.commit()
    return jsonify({'data':product_image.serialize(), 'message': f'product_image with id {id} modified'}), 200

#Delete product_image 
@api.route('/product_images/<int:id>', methods=['DELETE'])
def delete_product_image(id):
    stmt = select(Product_images).where(Product_images.id == id)
    product_image = db.session.execute(stmt).scalar_one_or_none()
    if product_image is None:
        return jsonify({'error': f'product_image with id {id} not found'}), 404
    db.session.delete(product_image)
    db.session.commit()
    return jsonify({'message': f'product_image with id {id} deleted'}), 200

#Get all purchases
@api.route('/purchases', methods=['GET'])
def get_purchases():
    stmt =select(Purchases)
    purchases = db.session.execute(stmt).scalars().all()
    return jsonify([purchase.serialize() for purchase in purchases]), 200

#Get single purchase
@api.route('/purchases/<int:id>', methods=['GET'])
def get_single_purchase(id):
    stmt = select(Purchases).where(Purchases.id == id)
    purchase = db.session.execute(stmt).scalar_one_or_none()
    if purchase is None:
        return jsonify({'error' : f'purchase with id {id} not found'}), 404 
    return jsonify(purchase.serialize()), 200


#Post purchase (create purchase)
@api.route('/purchases', methods=['POST'])
def create_purchase():
    data= request.get_json()
    if not data or 'product_id' not in data or 'buyer_id' not in data or 'seller_id' not in data:
        return jsonify({'error': 'missing data to create a purchase'}), 400
  
    new_purchase = Purchases(
        product_id=data['product_id'],
        buyer_id=data['buyer_id'],
        seller_id=data['seller_id']       
    )
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify(new_purchase.serialize()), 201

#Put purchase (modify purchase)
@api.route('/purchases/<int:id>', methods=['PUT'])
def update_purchase(id):
    data = request.get_json()
    stmt = select(Purchases).where(Purchases.id == id)
    purchase= db.session.execute(stmt).scalar_one_or_none()
    if purchase is None:
        return jsonify({'error': f'purchase {id} not found'}), 404
    purchase.product_id = data.get('product_id', purchase.product_id)
    purchase.buyer_id = data.get('buyer_id', purchase.buyer_id)
    purchase.seller_id = data.get('seller_id', purchase.seller_id)
    db.session.commit()
    return jsonify({'data':purchase.serialize(), 'message': f'purchase with id {id} modified'}), 200

#Delete purchase 
@api.route('/purchases/<int:id>', methods=['DELETE'])
def delete_purchase(id):
    stmt = select(Purchases).where(Purchases.id == id)
    purchase = db.session.execute(stmt).scalar_one_or_none()
    if purchase is None:
        return jsonify({'error': f'purchase with id {id} not found'}), 404
    db.session.delete(purchase)
    db.session.commit()
    return jsonify({'message': f'purchase with id {id} deleted'}), 200

#Get all ratings
@api.route('/ratings', methods=['GET'])
def get_ratings():
    stmt =select(Ratings)
    ratings = db.session.execute(stmt).scalars().all()
    return jsonify([rating.serialize() for rating in ratings]), 200

#Get single rating
@api.route('/ratings/<int:id>', methods=['GET'])
def get_single_rating(id):
    stmt = select(Ratings).where(Ratings.id == id)
    rating = db.session.execute(stmt).scalar_one_or_none()
    if rating is None:
        return jsonify({'error' : f'rating with id {id} not found'}), 404 
    return jsonify(rating.serialize()), 200

#Get ratings recieved by user
@api.route('/ratings/user/<int:user_id>', methods=['GET'])
def get_ratings_by_user(user_id):
    stmt = select(Ratings).where(Ratings.to_user_id == user_id)
    ratings = db.session.execute(stmt).scalars().all()
    return jsonify([rating.serialize() for rating in ratings]), 200

#Get ratings given by user
@api.route('/ratings/user/<int:user_id>/given', methods=['GET'])
def get_ratings_given_by_user(user_id):
    stmt = select(Ratings).where(Ratings.from_user_id == user_id)
    ratings = db.session.execute(stmt).scalars().all()
    return jsonify([rating.serialize() for rating in ratings]), 200

#Post rating (create rating)
@api.route('/ratings', methods=['POST'])
def create_rating():
    data= request.get_json()
    if not data or 'purchase_id' not in data or 'from_user_id' not in data or 'to_user_id' not in data or 'product_rating' not in data or 'user_rating' not in data or 'comment' not in data:
        return jsonify({'error': 'missing data to create a rating'}), 400
  
    new_rating = Ratings(
        purchase_id=data['purchase_id'],
        from_user_id=data['from_user_id'],
        to_user_id=data['to_user_id'],     
        product_rating=data['product_rating'],
        user_rating=data['user_rating'],
        comment=data['comment'] 
    )
    db.session.add(new_rating)
    db.session.commit()
    return jsonify(new_rating.serialize()), 201

#Put rating (modify rating)
@api.route('/ratings/<int:id>', methods=['PUT'])
def update_rating(id):
    data = request.get_json()
    stmt = select(Ratings).where(Ratings.id == id)
    rating= db.session.execute(stmt).scalar_one_or_none()
    if rating is None:
        return jsonify({'error': f'rating {id} not found'}), 404
    rating.purchase_id = data.get('purchase_id', rating.purchase_id)
    rating.from_user_id = data.get('from_user_id', rating.from_user_id)
    rating.product_rating = data.get('product_rating', rating.product_rating)
    rating.user_rating = data.get('user_rating', rating.user_rating)
    rating.comment = data.get('comment', rating.comment)
    
    db.session.commit()
    return jsonify({'data':rating.serialize(), 'message': f'rating with id {id} modified'}), 200

#Delete rating 
@api.route('/ratings/<int:id>', methods=['DELETE'])
def delete_rating(id):
    stmt = select(Ratings).where(Ratings.id == id)
    rating = db.session.execute(stmt).scalar_one_or_none()
    if rating is None:
        return jsonify({'error': f'rating with id {id} not found'}), 404
    db.session.delete(rating)
    db.session.commit()
    return jsonify({'message': f'rating with id {id} deleted'}), 200


#Delete rating recieved by an user
@api.route('/ratings/user/<int:user_id>', methods=['DELETE'])
def delete_ratings_received_by_user(user_id):
    stmt = select(Ratings).where(Ratings.to_user_id == user_id)
    ratings = db.session.execute(stmt).scalars().all()
    if not ratings:
        return jsonify({'error': f'no ratings found for user with id {user_id}'}), 404
    
    for rating in ratings:
        db.session.delete(rating)
    db.session.commit()
    
    return jsonify({'message': f'all ratings received by user with id {user_id} have been deleted'}), 200

#Delete rating given by an user
@api.route('/ratings/user/<int:user_id>/given', methods=['DELETE'])
def delete_ratings_given_by_user(user_id):
    stmt = select(Ratings).where(Ratings.from_user_id == user_id)
    ratings = db.session.execute(stmt).scalars().all()
    if not ratings:
        return jsonify({'error': f'no ratings given by user with id {user_id} found'}), 404
    
    for rating in ratings:
        db.session.delete(rating)
    db.session.commit()
    
    return jsonify({'message': f'all ratings given by user with id {user_id} have been deleted'}), 200


#Get all categories
@api.route('/categories', methods=['GET'])
def get_categories():
    stmt =select(Categories)
    categories = db.session.execute(stmt).scalars().all()
    return jsonify([category.serialize() for category in categories]), 200

#Get single category
@api.route('/categories/<int:id>', methods=['GET'])
def get_single_category(id):
    stmt = select(Categories).where(Categories.id == id)
    category = db.session.execute(stmt).scalar_one_or_none()
    if category is None:
        return jsonify({'error' : f'category with id {id} not found'}), 404 
    return jsonify(category.serialize()), 200

#Get subcategories
@api.route('/categories/<int:id>/children', methods=['GET'])
def get_category_children(id):
    stmt = select(Categories).where(Categories.parent_id == id)
    children = db.session.execute(stmt).scalars().all()
    return jsonify([child.serialize() for child in children]), 200


#Post category (create category)
@api.route('/categories', methods=['POST'])
def create_category():
    data= request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'missing data to create a category'}), 400
  
    new_category = Categories(
        name=data['name'],
        parent_id=data.get('parent_id')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.serialize()), 201

#Put category (modify category)
@api.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    stmt = select(Categories).where(Categories.id == id)
    category= db.session.execute(stmt).scalar_one_or_none()
    if category is None:
        return jsonify({'error': f'category {id} not found'}), 404
    category.name = data.get('name', category.name)
    category.parent_id = data.get('parent_id', category.parent_id) 
    db.session.commit()
    return jsonify({'data':category.serialize(), 'message': f'category with id {id} modified'}), 200

#Delete category 
@api.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    stmt = select(Categories).where(Categories.id == id)
    category = db.session.execute(stmt).scalar_one_or_none()
    if category is None:
        return jsonify({'error': f'category with id {id} not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': f'category with id {id} deleted'}), 200

#Get all favorites
@api.route('/favorites', methods=['GET'])
def get_favorites():
    stmt =select(Favorites)
    favorites = db.session.execute(stmt).scalars().all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

#Get specific favorite
@api.route('/favorites/<int:favorite_id>', methods=['GET'])
def get_specific_favorite(favorite_id):
    favorite = db.session.get(Favorites, favorite_id)
    if not favorite:
        return jsonify({'error': f'favorite with id {favorite_id} not found'}), 404
    return jsonify(favorite.serialize()), 200


#Get all favorites from user
@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    stmt = select(Favorites).where(Favorites.user_id == user_id)
    favorites = db.session.execute(stmt).scalars().all()
    if not favorites:
        return jsonify({'error' : f'favorites of user {user_id} not found'}), 404 
    return jsonify([favorite.serialize() for favorite in favorites]), 200

#Get one favorite from user
@api.route('/users/<int:user_id>/favorites/<int:id>', methods=['GET'])
def get_user_single_favorite(user_id, id):
    stmt = select(Favorites).where(Favorites.id == id, Favorites.user_id == user_id)
    favorite = db.session.execute(stmt).scalar_one_or_none()
    if favorite is None:
        return jsonify({'error': f'Favorite with id {id} for user {user_id} not found'}), 404
    return jsonify(favorite.serialize()), 200

#Post favorite for an user (create favorite for an user)
@api.route('/users/<int:user_id>/favorites', methods=['POST'])
def create_user_favorite(user_id):
    data= request.get_json()
    if not data or 'product_id' not in data:
        return jsonify({'error': 'missing product_id to create a favorite'}), 400
    #Validate user
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': f'user with id {user_id} not found'}), 404
  
    new_favorite = Favorites(
        user_id=user_id,
        product_id=data['product_id']
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201


#Put favorite for an user (modify favorite of an user)
@api.route('/users/<int:user_id>/favorites/<int:id>', methods=['PUT'])
def update_user_favorite(user_id, id):
    data = request.get_json()
    stmt = select(Favorites).where(Favorites.id == id, Favorites.user_id == user_id)
    favorite= db.session.execute(stmt).scalar_one_or_none()
    if favorite is None:
        return jsonify({'error': f'favorite with id {id} for user {user_id} not found'}), 404
    favorite.product_id = data.get('product_id', favorite.product_id)
    db.session.commit()
    return jsonify({'data': favorite.serialize(), 'message': f'favorite with id {id} for user {user_id} modified'}), 200

#Delete gobal favorite  by id
@api.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    stmt = select(Favorites).where(Favorites.id == id)
    favorite = db.session.execute(stmt).scalar_one_or_none()
    if favorite is None:
        return jsonify({'error': f'favorite with id {id} not found'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': f'favorite with id {id} deleted'}), 200

#Delete favorite from user 
@api.route('/users/<int:user_id>/favorites/<int:id>', methods=['DELETE'])
def delete_user_favorite(user_id, id):
    stmt = select(Favorites).where(Favorites.id == id, Favorites.user_id == user_id)
    favorite = db.session.execute(stmt).scalar_one_or_none()
    if favorite is None:
        return jsonify({'error': f'favorite with id {id} for user {user_id} not found'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': f'favorite with id {id} for user {user_id} deleted'}), 200

#Averages and stats
#Rating average for a product
@api.route('/stats/product/<int:product_id>/average_rating', methods=['GET'])
def average_rating_product(product_id):
    ratings = Ratings.query.filter_by(product_id=product_id).all()
    if not ratings:
        return jsonify({'error': 'no ratings found for this product'}), 404
    
    avg_rating = sum(r.score for r in ratings) / len(ratings)
    return jsonify({'product_id': product_id, 'average_rating': avg_rating})

#Rating average for an user
@api.route('/stats/user/<int:user_id>/average_rating', methods=['GET'])
def average_rating_user(user_id):
    ratings = Ratings.query.filter_by(user_id=user_id).all()
    if not ratings:
        return jsonify({'error': 'no ratings found for this user'}), 404
    
    avg_rating = sum(r.score for r in ratings) / len(ratings)
    return jsonify({'user_id': user_id, 'average_rating': avg_rating})

# Amount of purchases for an user
@api.route('/stats/user/<int:user_id>/purchase_count', methods=['GET'])
def purchase_count_user(user_id):
    purchase_count = Purchases.query.filter_by(user_id=user_id).count()
    return jsonify({'user_id': user_id, 'purchase_count': purchase_count})

# Amount of purchases for an product
@api.route('/stats/product/<int:product_id>/purchase_count', methods=['GET'])
def purchase_count_product(product_id):
    purchase_count = Purchases.query.filter_by(product_id=product_id).count()
    return jsonify({'product_id': product_id, 'purchase_count': purchase_count})
