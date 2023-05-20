import math
import numpy as np
import pandas as pd

class ClientA(Client):
    def __init__(self, X, config):
        super().__init__(config)
        self.X = X
        self.weights = np.zeros(X.shape[1])
        
    def compute_z_a(self):
        z_a = np.dot(self.X, self.weights)
        return z_a
    
	## 加密梯度的计算，对应step4
    def compute_encrypted_dJ_a(self, encrypted_u):
        encrypted_dJ_a = self.X.T.dot(encrypted_u) + self.config['lambda'] * self.weights
        return encrypted_dJ_a
    
	##参数的更新
    def update_weight(self, dJ_a):
        self.weights = self.weights - self.config["lr"] * dJ_a / len(self.X)
        return

    ## A: step2
    def task_1(self, client_B_name):
        dt = self.data
        assert "public_key" in dt.keys(), "Error: 'public_key' from C in step 1 not successfully received."
        public_key = dt['public_key']
        z_a = self.compute_z_a()
        u_a = 0.25 * z_a
        z_a_square = z_a ** 2
        encrypted_u_a = np.asarray([public_key.encrypt(x) for x in u_a])
        encrypted_z_a_square = np.asarray([public_key.encrypt(x) for x in z_a_square])
        dt.update({"encrypted_u_a": encrypted_u_a})
        data_to_B = {"encrypted_u_a": encrypted_u_a, "encrypted_z_a_square": encrypted_z_a_square}
        self.send_data(data_to_B, self.other_client[client_B_name])
    
    ## A: step3、4
    def task_2(self, client_C_name):
        dt = self.data
        assert "encrypted_u_b" in dt.keys(), "Error: 'encrypted_u_b' from B in step 1 not successfully received."
        encrypted_u_b = dt['encrypted_u_b']
        encrypted_u = encrypted_u_b + dt['encrypted_u_a']
        encrypted_dJ_a = self.compute_encrypted_dJ_a(encrypted_u)
        mask = np.random.rand(len(encrypted_dJ_a))
        encrypted_masked_dJ_a = encrypted_dJ_a + mask
        dt.update({"mask": mask})
        data_to_C = {'encrypted_masked_dJ_a': encrypted_masked_dJ_a}
        self.send_data(data_to_C, self.other_client[client_C_name])
       
    ## A: step6
    def task_3(self):
        dt = self.data
        assert "masked_dJ_a" in dt.keys(), "Error: 'masked_dJ_a' from C in step 2 not successfully received."
        masked_dJ_a = dt['masked_dJ_a']
        dJ_a = masked_dJ_a - dt['mask']
        self.update_weight(dJ_a)
        print(f"A weight: {self.weights}")
        return
    
    def L2_clip(v, b):
        norm = np.linalg.norm(v)
        if norm > b:
            return b*(v/norm)
        else:
            return v
    
    def compute_sensitivity(self):
        # compute sensitivity using L2 norm, parameter b is the bound
        b = 0.5
        X_a = self.X
        X_a_modified = X_a + np.random.gauss(0, b, X_a.shape)
        Y_a = np.dot(X_a, self.weights)
        Y_a_modified = np.dot(X_a_modified, self.weights)
        sensitivity = self.L2_clip(Y_a - Y_a_modified, b)
        return sensitivity
    
    def get_sigma(self, sensitivity):
        sigma = math.sqrt(2 * sensitivity**2 * math.log(1.25 / self.config['delta'] ) / (self.config['epsilon']**2))
        return sigma
    
config = {
    "lr": 0.01,
    "lambda": 0.01,
    "delta": 1e-5,
    "epsilon": 0.1,
    "delta": 1e-5
}