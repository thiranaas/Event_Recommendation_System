const {
  getAllEvents,
  getEventById,
  createEvent,
  updateEvent,
  deleteEvent,
  searchEvents,
  getEventsByCategory,
} = require("../../db/queries/eventQueries");

const getEvents = async (req, res) => {
  try {
    const events = await getAllEvents();

    res.status(200).json({
      success: true,
      data: events,
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: "Failed to fetch events",
    });
  }
};

const getEvent = async (req, res) => {
  try {
    const event = await getEventById(req.params.id);

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    res.status(200).json({
      success: true,
      data: event,
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: "Failed to fetch event",
    });
  }
};

const createEventController = async (req, res) => {
  try {
    const event = await createEvent(req.body);

    res.status(201).json({
      success: true,
      message: "Event created successfully",
      data: event,
    });
  } catch (error) {
    console.error(error);

    res.status(error.status || 500).json({
      success: false,
      message: error.status ? error.message : "Failed to create event",
    });
  }
};

const updateEventController = async (req, res) => {
  try {
    const event = await getEventById(req.params.id);

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    const updatedEvent = await updateEvent(
      req.params.id,
      req.body
    );

    res.status(200).json({
      success: true,
      message: "Event updated successfully",
      data: updatedEvent,
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: "Failed to update event",
    });
  }
};

const deleteEventController = async (req, res) => {
  try {
    const event = await getEventById(req.params.id);

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    await deleteEvent(req.params.id);

    res.status(200).json({
      success: true,
      message: "Event deleted successfully",
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: "Failed to delete event",
    });
  }
};

const searchEventsController = async (req, res) => {
  try {
    const query = req.query.q;

    if (!query || !query.trim()) {
      return res.status(400).json({
        success: false,
        message: "Search query is required",
      });
    }

    const events = await searchEvents(query.trim());

    res.status(200).json({
      success: true,
      data: events,
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: "Failed to search events",
    });
  }
};

const getEventsByCategoryController = async (req, res) => {
  try {
    const events = await getEventsByCategory(req.params.category);

    res.status(200).json({
      success: true,
      data: events,
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: "Failed to fetch events by category",
    });
  }
};

module.exports = {
  getEvents,
  getEvent,
  createEventController,
  updateEventController,
  deleteEventController,
  searchEventsController,
  getEventsByCategoryController,
};
