// TODO: seed the DB using Prisma
const prisma = require("./client");

async function seed() {
    console.log("Seeding the database.");
    await prisma.faceShape.deleteMany();



    // <------------------------ HOMEPAGE ------------------------>


    try {
        const diamond = await prisma.faceShape.create({
            data: {
                name: "Diamond"
            }
        })


    }


    // <------------------------ FACE SHAPE ------------------------>



    // <---- DIAMOND ---->


    // <---- HEART ---->

    // <---- ROUND ---->

    // <---- OVAL ---->

    // <---- SQUARE ---->

    // <---- TRIANGLE ---->






    // <------------------------ SKIN TONE ------------------------>



    // <---- SKIN TONE: FAIR ---->

    // <---- SKIN TONE: LIGHT ---->

    // <---- SKIN TONE: LIGHT MEDIUM  ---->

    // <---- SKIN TONE: MEDIUM  ---->

    // <---- SKIN TONE: MEDIUM TAN ---->

    // <---- SKIN TONE: TAN ---->

    // <---- SKIN TONE: TAN DARK ---->

    // <---- SKIN TONE: DARK ---->

    // <---- SKIN TONE: DARK DEEP ---->

    // <---- SKIN TONE: DEEP ---->

    catch (error) {
        console.error(error);
    }
    console.log("Seeded Database.")
}



seed().then(async () => {
    await prisma.$disconnect();
}).catch(async (e) => {
    console.error(e)
    await prisma.$disconnect();
    process.exit(1)
})




