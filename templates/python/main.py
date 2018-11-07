


if __name__ == '__main__':
    {% if python_ver == 'python3' or not python_ver %}
        print("Hello {{ username }}")
    {% else %}
        print "Hello {{ username }}"
    {% endif %}
