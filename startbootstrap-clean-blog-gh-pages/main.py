import requests
from flask import Flask, render_template
from flask import request
import smtplib

app = Flask(__name__)
URL = 'https://api.npoint.io/c790b4d5cab58020d391'
response = requests.get(url=URL)
all_posts = response.json()
MY_EMAIL = 'kodiugos@gmail.com'
PWD = 'llhytkakbfhnikci'


@app.route('/index')
def home():
    return render_template('index.html', posts=all_posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone_no']
        message = request.form['msg']
        # print(name, email, phone, message)
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            # Secure the connection
            connection.starttls()
            # login the user
            connection.login(user=MY_EMAIL, password=PWD)
            # send email
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f'Subject:Contact Message Alert!!!.\n\nName: {name}\n\nEmail: {email}\n\nPhone number: {phone}'
                    f'\n\nMessage: {message}'
                .encode("utf-8")
            )
        return render_template('contact.html', success=True)
    else:
        return render_template('contact.html', success=False)


@app.route('/post/<int:post_id>')
def get_post(post_id):
    for post in all_posts:
        if post['id'] == post_id:
            title = post['title']
            subtitle = post['subtitle']
            body = post['body']
            return render_template('post.html', title=title, subtitle=subtitle, body=body)


if __name__ == "__main__":
    app.run(debug=True)
