from cloud_auth import SignedRequestAuth


def get_instances(user):
    print('get_instances')
    print(user)

    private_key = ''
    try:
        with open(user.private_key_path) as f:
            private_key = f.read()
            print(private_key)
    except BaseException as e:
        print('Error: ' + str(e))

    api_key = "/".join([
    user.tenancy_ocid,
    user.user_ocid,
    user.fingerprint
    ])
    print(api_key)

    print('SignedRequestAuth enter')
    auth = SignedRequestAuth(api_key, private_key)
    headers = {
    "content-type": "application/json",
    "date": email.utils.formatdate(usegmt=True),
    }
    print('exit')

    # GET with query parameters
    uri = "https://iaas.us-phoenix-1.oraclecloud.com/20160918/instances?availabilityDomain={availability_domain}&compartmentId={compartment_id}"
    uri = uri.format(
    availability_domain="Lgmh:PHX-AD-1".replace(":", "%3A"),
    compartment_id="ocid1.compartment.oc1..aaaaaaaav2n5hgf5jkd2x3jnwei7dgffdr2awqe5joykt2ma76nz7pzdxyca".replace(":", "%3A")

    )
    print('querying OCI api')
    response = requests.get(uri, auth=auth, headers=headers)
    print(response.status_code)
    print(response.text)
    return response.json()
