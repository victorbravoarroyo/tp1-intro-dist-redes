import connexion

app = connexion.App(__name__, specification_dir='./api')
app.add_api('swagger.yml')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
