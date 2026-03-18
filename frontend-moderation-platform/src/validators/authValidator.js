export const validateLogin = (user_id, region) => {
  const errors = [];

  if (!user_id) {
    errors.push("User ID is required");
  } else {
    if (user_id.length > 8) {
      errors.push("User ID can be 8 characters");
    }
    const regex = /^[a-zA-Z0-9]+$/;
    if (!regex.test(user_id)) {
      errors.push("User ID cannot contain special characters");
    }
  }

  if (!region) {
    errors.push("Please select a region");
  }

  return errors;
};
