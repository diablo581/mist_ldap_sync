from req import mist_get, mist_delete, mist_post
import random
import string

class Mist():
    def __init__(self, config):
        self.host = config.get("host")
        self.apitoken = config.get("api_token")
        self.scope = config.get("scope")
        self.scope_id = config.get("scope_id")
        self.ssid = config.get("ssid")
        self.psk_length = config.get("psk_length")
        self.psk_vlan = config.get("psk_vlan")
        self.psk_max_usage = config.get("psk_max_usage")
        self.allowed_chars = config.get("allowed_chars")
        self.excluded_psks = config.get("excluded_psks")
        
    def _get_random_alphanumeric_string(self):
        result_str = ''.join((random.choice(self.allowed_chars) for i in range(self.psk_length)))
        return result_str

    def get_users(self, mist_user_list=[]):
        print(f"Requesting {self.host} to get the list of PSKs ".ljust(79, "."), end="", flush=True)
        try:
            res = self.get_ppks()
            if "result" in res:
                for psk in res["result"]:
                    mist_user_list.append({"name": psk["name"], "id": psk["id"]})
            print("\033[92m\u2714\033[0m")
            return mist_user_list
        except:
            print('\033[31m\u2716\033[0m')
            exit(2)

    def get_ppks(self):
        url = f"https://{self.host}/api/v1/{self.scope}/{self.scope_id}/psks"
        response = mist_get(self.apitoken, url, query={"ssid": self.ssid}, limit=1000)
        return response

    def delete_ppsk(self, psk_id, dry_run:bool=False):
        if dry_run:
            return True
        else:
            url =  f"https://{self.host}/api/v1/{self.scope}/{self.scope_id}/psks/{psk_id}"
            response = mist_delete(self.apitoken, url)
            return response
        

    def create_ppsk(self, user, dry_run:bool=False):
        print("    Creating the PPSK for user ".ljust(79, "."), end="", flush=True)
        psk = self._get_random_alphanumeric_string()
        psk_data = {
            "usage": "multi",
            "name": user["name"],
            "ssid": self.ssid,
            "vlan_id": self.psk_vlan,
            "passphrase": psk,
            "max_usage": self.psk_max_usage
        }
        try:
            if dry_run:
                res = psk_data
                res["id"] = 1
            else:
                url =  f"https://{self.host}/api/v1/{self.scope}/{self.scope_id}/psks"
                res = mist_post(self.apitoken, url, psk_data)["result"] 
            if "id" in res and "ssid" in res and "passphrase" in res:       
                print("\033[92m\u2714\033[0m")
                return res
            else:
                print('\033[31m\u2716\033[0m')
                return None
        except:
            print('\033[31m\u2716\033[0m')
            return None


        
 
