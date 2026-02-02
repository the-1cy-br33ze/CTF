from flask import Flask, request, Response

app = Flask(__name__)

ADDITIONS = ["cream", "syrup", "whisky"]
brewing = False

@app.route('/coffee', methods=['BREW', 'POST', 'PROPFIND', 'WHEN'])
def coffee_handler():
    global brewing

    # PROPFIND: Get additions list (RFC 2.1.3)
    if request.method == 'PROPFIND':
        return Response(
            f'<D:additions>{" ".join(ADDITIONS)}</D:additions>\n',
            status=207,
            headers={'Content-Type': 'application/xml', 'Safe': 'yes'}
        )

    # BREW/POST: Start brewing (RFC 2.1.1, 2.2)
    if request.method in ['BREW', 'POST']:
        brewing = True

        # Validate Content-Type (RFC 2.1.1)
        if request.headers.get('Content-Type') != 'application/coffee-pot-command':
            return Response(
                "Error 400: Invalid Content-Type (RFC 2.1.1)\n",
                status=400,
                headers={'Safe': 'no'}
            )

        # Validate command body (RFC 4)
        if request.get_data(as_text=True).strip() != 'start':
            return Response(
                "Error 400: Invalid command (RFC 4)\n",
                status=400,
                headers={'Safe': 'no'}
            )

        # Validate Accept-Additions (RFC 2.2.2.1)
        accept_additions = request.headers.get('Accept-Additions', '')
        if not all(addition in ADDITIONS for addition in accept_additions.split(', ')):
            return Response(
                "Error 406: Unacceptable additions (RFC 2.2.2.1)\n",
                status=406,
                headers={'Safe': 'no', 'Accept-Additions': ', '.join(ADDITIONS)}
            )

        return Response(
            "Brewing started\n",
            status=202,
            headers={'Safe': 'conditionally-safe'}
        )

    # WHEN: Finish brewing (RFC 2.1.4)
    if request.method == 'WHEN' and brewing:
        brewing = False
        return Response(
            "Coffee ready! Flag: flag{1t_w@sn't_a_j0ke}\n",
            status=200,
            headers={'Safe': 'yes'}
        )

    return Response("Error 405: Method not allowed\n", status=405)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def teapot(path):
    return Response("418 I'm a teapot. Read the RFC.\n", status=418)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)