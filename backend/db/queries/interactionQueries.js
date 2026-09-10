const prisma = require("../connection");
const createInteraction = async ({ userId, eventId, type }) => {
  return await prisma.interaction.create({
    data: {
      userId: Number(userId),
      eventId: Number(eventId),
      type: type
    }
  });
};
const getUserInteractions = async (userId) => {
  return await prisma.interaction.findMany({
    where: {
      userId: Number(userId)
    },
    include: {
      event: true
    },
    orderBy: {
      createdAt: "desc"
    }
  });
};
const getEventInteractions = async (eventId) => {
  return await prisma.interaction.findMany({
    where: {
      eventId: Number(eventId)
    },
    include: {
      user: true
    }
  });
};
const getUserInteractionsByType = async (userId, type) => {
  return await prisma.interaction.findMany({
    where: {
      userId: Number(userId),
      type: type
    },
    include: {
      event: true
    }
  });
};
const deleteInteraction = async (id) => {
  return await prisma.interaction.delete({
    where: {
      id: Number(id)
    }
  });
};

module.exports = {
  createInteraction,
  getUserInteractions,
  getEventInteractions,
  getUserInteractionsByType,
  deleteInteraction
};