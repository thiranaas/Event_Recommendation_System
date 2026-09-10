const prisma = require("../connection");
const createSearchHistory = async ({ userId, query }) => {
  return await prisma.searchHistory.create({
    data: {
      userId: Number(userId),
      query: query
    }
  });
};
const getUserSearchHistory = async (userId) => {
  return await prisma.searchHistory.findMany({
    where: {
      userId: Number(userId)
    },
    orderBy: {
      createdAt: "desc"
    }
  });
};
const getRecentSearches = async (userId, limit = 10) => {
  return await prisma.searchHistory.findMany({
    where: {
      userId: Number(userId)
    },
    orderBy: {
      createdAt: "desc"
    },
    take: Number(limit)
  });
};
const deleteUserSearchHistory = async (userId) => {
  return await prisma.searchHistory.deleteMany({
    where: {
      userId: Number(userId)
    }
  });
};

module.exports = {
  createSearchHistory,
  getUserSearchHistory,
  getRecentSearches,
  deleteUserSearchHistory
};