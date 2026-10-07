import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const registerUser = (data) => {
  return api.post("/auth/register", data);
};

export const loginUser = (data) => {
  return api.post("/auth/login", data);
};

export const getProducts = () => {
  return api.get("/products/");
};

export const addToCart = (data, token) => {
  return api.post("/cart/", data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const getCart = (token) => {
  return api.get("/cart/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const removeFromCart = (productId, token) => {
  return api.delete(`/cart/${productId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const checkout = (token) => {
  return api.post(
    "/orders/checkout",
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};

export const getOrders = (token) => {
  return api.get("/orders/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const getNotifications = (token) => {
  return api.get("/notifications/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const markNotificationRead = (notificationId, token) => {
  return api.patch(
    `/notifications/${notificationId}/read`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};

export const createPayment = (orderId, token) => {
  return api.post(
    `/payments/checkout/${orderId}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};

export const failPayment = (orderId, token) => {
  return api.post(
    `/payments/fail/${orderId}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};

export default api;