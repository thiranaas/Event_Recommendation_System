const prisma = require("./connection");
const bcrypt = require("bcryptjs");
const seedEvents = require("./seedEvents.json");

async function main() {
  const eventCount = await prisma.event.count();

  if (eventCount === 0) {
    await prisma.event.createMany({
      data: seedEvents.map((event) => ({
        ...event,
        date: new Date(event.date),
        skills: event.skills || [],
        interests: event.interests || [],
        eventType: event.eventType || "Workshop",
        mode: event.mode || "Online"
      }))
    });
    console.log(`Seeded ${seedEvents.length} events.`);
  } else {
    console.log(`Skipping event seed, ${eventCount} events already exist.`);
  }
  const admins = [
    {
      name: "Vectored Admin",
      email: "dharaneesh@gmail.com",
      password: "dharaneesh_07"
    },
    {
      name: "Vectored Admin",
      email: "praneethan@gmail.com",
      password: "praneethan_07"
    }
  ];

  for (const admin of admins) {
    const existing = await prisma.user.findUnique({
      where: { email: admin.email }
    });

    if (existing) continue;

    await prisma.user.create({
      data: {
        name: admin.name,
        email: admin.email,
        password: await bcrypt.hash(admin.password, 10),
        role: "ADMIN",
        preferredMode: "Online",
        preferredEventType: [],
        skills: [],
        interests: []
      }
    });

    console.log(`Created admin account: ${admin.email}`);
  }

  console.log("Database is ready.");
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
