const prisma = require("../connection");

const parseOptionalNumber = (value, fieldName) => {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    const error = new Error(`${fieldName} must be a valid number`);
    error.status = 400;
    throw error;
  }

  return parsed;
};

const parseOptionalDate = (value, fieldName) => {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    const error = new Error(`${fieldName} must be a valid date`);
    error.status = 400;
    throw error;
  }

  return parsed;
};

const getAllEvents = async () => {
  return await prisma.event.findMany({
    orderBy: {
      date: "asc",
    },
  });
};

const getEventById = async (id) => {
  return await prisma.event.findUnique({
    where: {
      id: Number(id)
    }
  });
};

const searchEvents = async (search) => {
  return await prisma.event.findMany({
    where: {
      OR: [
        {
          title: {
            contains: search,
            mode: "insensitive"
          }
        },
        {
          description: {
            contains: search,
            mode: "insensitive"
          }
        },
        {
          location: {
            contains: search,
            mode: "insensitive"
          }
        },
        {
          domain: {
            contains: search,
            mode: "insensitive"
          }
        }
      ]
    },
    orderBy: {
      date: "asc"
    }
  });
};

const getEventsByCategory = async (category) => {
  return await prisma.event.findMany({
    where: {
      domain: {
        equals: category,
        mode: "insensitive"
      }
    },
    orderBy: {
      date: "asc"
    }
  });
};

const createEvent = async (data) => {
  if (!data || typeof data.title !== "string" || !data.title.trim()) {
    const error = new Error("Title is required");
    error.status = 400;
    throw error;
  }

  return await prisma.event.create({
    data: {
      title: data.title.trim(),
      date: parseOptionalDate(data.date, "date"),
      location: data.location,
      domain: data.domain,
      eventType: data.eventType || "Workshop",
      mode: data.mode || (data.location && data.location.toLowerCase() === "online" ? "Online" : "Offline"),
      skills: Array.isArray(data.skills) ? data.skills : [],
      interests: Array.isArray(data.interests) ? data.interests : [],
      startTime: data.startTime,
      endTime: data.endTime,
      registrationFee: parseOptionalNumber(data.registrationFee, "registrationFee"),
      cashPrize: parseOptionalNumber(data.cashPrize, "cashPrize"),
      certificateAvailable: data.certificateAvailable || false,
      posterUrl: data.posterUrl,
      registrationUrl: data.registrationUrl,
      whatsappGroupLink: data.whatsappGroupLink,
      contactNumber: data.contactNumber,
      contactEmail: data.contactEmail,
      organizerName: data.organizerName,
      organizerDepartment: data.organizerDepartment,
      description: data.description,
      registrationDeadline: parseOptionalDate(
        data.registrationDeadline,
        "registrationDeadline"
      )
    }
  });
};

const updateEvent = async (id, data) => {
  return await prisma.event.update({
    where: {
      id: Number(id)
    },
    data: {
      title: data.title,
      date: data.date ? new Date(data.date) : undefined,
      location: data.location,
      domain: data.domain,
      eventType: data.eventType,
      mode: data.mode,
      skills: Array.isArray(data.skills) ? data.skills : undefined,
      interests: Array.isArray(data.interests) ? data.interests : undefined,
      startTime: data.startTime,
      endTime: data.endTime,
      registrationFee: data.registrationFee,
      cashPrize: data.cashPrize,
      certificateAvailable: data.certificateAvailable,
      posterUrl: data.posterUrl,
      registrationUrl: data.registrationUrl,
      whatsappGroupLink: data.whatsappGroupLink,
      contactNumber: data.contactNumber,
      contactEmail: data.contactEmail,
      organizerName: data.organizerName,
      organizerDepartment: data.organizerDepartment,
      description: data.description,
      registrationDeadline: data.registrationDeadline
        ? new Date(data.registrationDeadline)
        : undefined
    }
  });
};

const deleteEvent = async (id) => {
  return await prisma.event.delete({
    where: {
      id: Number(id)
    }
  });
};

const deleteExpiredEvents = async () => {
  return await prisma.event.deleteMany({
    where: {
      date: {
        lt: new Date()
      }
    }
  });
};

module.exports = {
  getAllEvents,
  getEventById,
  searchEvents,
  getEventsByCategory,
  createEvent,
  updateEvent,
  deleteEvent,
  deleteExpiredEvents
};