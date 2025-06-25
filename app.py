from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
