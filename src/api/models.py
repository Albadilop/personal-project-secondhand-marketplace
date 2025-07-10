from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from flask import Flask

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=True)
    average_rating_as_seller: Mapped[Optional[float]] = mapped_column(nullable=True)
    average_rating_as_buyer: Mapped[Optional[float]] = mapped_column(nullable=True)
    avatar_url: Mapped[str] =mapped_column(String(1000),nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relatioships
    products: Mapped[List[Products]] = relationship('Products', back_populates='owner')
    favorites: Mapped[List[Favorites]] = relationship('Favorites', back_populates='user')



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "average_rating_as_seller": self.average_rating_as_seller,
            "average_rating_as_buyer": self.average_rating_as_buyer,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None
            # do not serialize the password, its a security breach
        }
    

class Products(db.Model):
    __tablename__= 'products'
    id: Mapped[int] =mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(1500), nullable=True)
    price: Mapped[int]=mapped_column(Integer, nullable=False)
    is_sold: Mapped[bool] = mapped_column(Boolean, nullable=True, server_default='false')
    owner_id: Mapped[int] =mapped_column(ForeignKey('users.id', ondelete='CASCADE'),nullable=False)
    category_id: Mapped[int]=mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    average_rating: Mapped[Optional[float]] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    #Relationships
    owner: Mapped[Users] = relationship('Users', back_populates='products')
    category: Mapped[Categories] = relationship('Categories', back_populates='products')
    images: Mapped[List[Product_images]] = relationship('Product_images', back_populates='product')
    favorites: Mapped[List[Favorites]] = relationship('Favorites', back_populates='product')


    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "is_sold": self.is_sold,
            "owner_id": self.owner_id,
            "category_id": self.category_id,
            "average_rating": self.average_rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
class Product_images(db.Model):
    __tablename__='product_images'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int]=mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    image_url: Mapped[str]= mapped_column(String(1000), nullable=False)

    #Relationship 
    product: Mapped[Products] = relationship('Products', back_populates='images')

    def serialize(self):
        return{
            "id": self.id,
            "product_id": self.product_id,
            "image_url": self.image_url,
        }
    
class Purchases(db.Model):
    __tablename__ = 'purchases'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    product: Mapped[Products] = relationship('Products')
    buyer: Mapped[Users] = relationship('Users', foreign_keys=[buyer_id])
    seller: Mapped[Users] = relationship('Users', foreign_keys=[seller_id])

    def serialize(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
class Ratings(db.Model):
    __tablename__ = 'ratings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('purchases.id', ondelete='CASCADE'), nullable=False)
    from_user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    to_user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # escala 1-5, por ejemplo
    user_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # escala 1-5
    comment: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    order: Mapped[Purchases] = relationship('Purchases')
    from_user: Mapped[Users] = relationship('Users', foreign_keys=[from_user_id])
    to_user: Mapped[Users] = relationship('Users', foreign_keys=[to_user_id])

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "product_rating": self.product_rating,
            "user_rating": self.user_rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Categories(db.Model):
    __tablename__='categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String(120), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)

    #Relationships
    parent: Mapped[Optional[Categories]] = relationship('Categories', remote_side=[id], backref='subcategories')
    products: Mapped[List[Products]] = relationship('Products', back_populates='category')

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
        }

class Favorites(db.Model):
    __tablename__= 'favorites'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)

    #Relationships
    user: Mapped[Users] = relationship('Users', back_populates='favorites')
    product: Mapped[Products] = relationship('Products', back_populates='favorites')

    def serialize(self):
        return{
            "user_id": self.user_id,
            "product_id": self.product_id
        }