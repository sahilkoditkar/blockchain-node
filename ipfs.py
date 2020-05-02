
import requests

class IPFS:

    pinata_api_key = "4ce3a7d51ec746ec3580"
    pinata_secret_api_key = "fdeadcdb93970485af97f6ef62ee177ea632a24f4c6bb81a77c218cfc0dba87d"

    #testAuthentication
    @staticmethod
    def isConnected():
        response = requests.get(url='https://api.pinata.cloud/data/testAuthentication', headers={
            "pinata_api_key": IPFS.pinata_api_key,
            "pinata_secret_api_key": IPFS.pinata_secret_api_key
        })
        print(response.status_code)
        print(response.headers)
        print(response.json())
        return response

    #pinList
    @staticmethod
    def getPinList():
        response = requests.get(url="https://api.pinata.cloud/data/pinList?status=pinned", headers={
            "pinata_api_key": IPFS.pinata_api_key,
            "pinata_secret_api_key": IPFS.pinata_secret_api_key
        })
        return response

    #userPinnedDataTotal
    @staticmethod
    def getPinnedDataTotal():
        response = requests.get(url="https://api.pinata.cloud/data/userPinnedDataTotal", headers={
            "pinata_api_key": IPFS.pinata_api_key,
            "pinata_secret_api_key": IPFS.pinata_secret_api_key
        })
        return response

    #pinJSONtoIPFS
    @staticmethod
    def addJson(jsonBlock):
        mydata = {
            "pinataContent": jsonBlock
        }
        response = requests.post(url="https://api.pinata.cloud/pinning/pinJSONToIPFS", json=mydata, headers={
            "Content-Type": "application/json",
            "pinata_api_key": IPFS.pinata_api_key,
            "pinata_secret_api_key": IPFS.pinata_secret_api_key
        })
        return response

    #getDataFromHash
    @staticmethod
    def getJson(IpfsHash):
        response = requests.get(f"https://gateway.pinata.cloud/ipfs/{IpfsHash}")
        return response

    #removePinFromIPFS
    @staticmethod
    def removeJson(IpfsHash):
        response = requests.post(url="https://api.pinata.cloud/pinning/removePinFromIPFS", data={"ipfs_pin_hash": IpfsHash}, headers={
            "pinata_api_key": IPFS.pinata_api_key,
            "pinata_secret_api_key": IPFS.pinata_secret_api_key
            })
        return response

