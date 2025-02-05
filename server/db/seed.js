// TODO: seed the DB using Prisma
const prisma = require("./client");

async function seed() {

    console.log("Seeding the database!");
    await prisma.faceShape.deleteMany();


    // <------------------------ FACE SHAPE ------------------------>

    try {
        // <---- DIAMOND ----> 
        const diamond = await prisma.faceShape.create({
            data: {
                name: "Diamond"
            }
        })

        // <---- HEART ----> 
        const heart = await prisma.faceShape.create({
            data: {
                name: "Heart"
            }
        })


        // <---- ROUND ----> 
        const round = await prisma.faceShape.create({
            data: {
                name: "Round"
            }
        })

        // <---- OVAL ----> 
        const oval = await prisma.faceShape.create({
            data: {
                name: "Oval"
            }
        })

        // <---- SQUARE ----> 
        const square = await prisma.faceShape.create({
            data: {
                name: "Square"
            }
        })

        // <---- TRIANGLE ----> 
        const triangle = await prisma.faceShape.create({
            data: {
                name: "Triangle"
            }
        })


        // <------------------------ SKIN TONE ------------------------>


        // <---- SKIN TONE: FAIR ---->
        const fair = await prisma.skinTone.create({
            data: {
                name: "Fair "
            }
        })

        // <---- SKIN TONE: FAIR LIGHT ---->
        const fairLight = await prisma.skinTone.create({
            data: {
                name: "Fair Light "
            }
        })

        // <---- SKIN TONE: LIGHT ---->
        const light = await prisma.skinTone.create({
            data: {
                name: "Light"
            }
        })

        // <---- SKIN TONE: LIGHT MEDIUM  ---->
        const lightMedium = await prisma.skinTone.create({
            data: {
                name: "Light Medium"
            }
        })


        // <---- SKIN TONE: MEDIUM  ---->
        const medium = await prisma.skinTone.create({
            data: {
                name: "Medium"
            }
        })


        // <---- SKIN TONE: MEDIUM TAN ---->
        const mediumTan = await prisma.skinTone.create({
            data: {
                name: "Medium Tan"
            }
        })


        // <---- SKIN TONE: TAN ---->
        const tan = await prisma.skinTone.create({
            data: {
                name: "Tan"
            }
        })


        // <---- SKIN TONE: TAN DARK ---->
        const tanDark = await prisma.skinTone.create({
            data: {
                name: "Tan Dark"
            }
        })


        // <---- SKIN TONE: DARK ---->
        const dark = await prisma.skinTone.create({
            data: {
                name: "Dark"
            }
        })


        // <---- SKIN TONE: DARK DEEP ---->
        const darkDeep = await prisma.skinTone.create({
            data: {
                name: "Dark Deep"
            }
        })


        // <---- SKIN TONE: DEEP ---->
        const deep = await prisma.skinTone.create({
            data: {
                name: "Deep"
            }
        })



        // <------------------------ SKIN TONE ------------------------>


        // <---- SKIN TYPE: DRY ---->

        const dry = await prisma.skinType.create({
            data: {
                name: "Dry"
            }
        })

        // <---- SKIN TYPE: COMBO ---->

        const combo = await prisma.skinType.create({
            data: {
                name: "Combo"
            }
        })


        // <---- SKIN TYPE: OILY ---->

        const oily = await prisma.skinType.create({
            data: {
                name: "Oily"
            }
        })


        // <---- SKIN TYPE: SENSITIVE ---->

        const sensitive = await prisma.skinType.create({
            data: {
                name: "Sensitive"
            }
        })


    }

    catch (error) {
        console.error(error);
    }
    console.log("Seeded Database!")

    seed().then(async () => {
        await prisma.$disconnect();
    }).catch(async (e) => {
        console.error(e)
        await prisma.$disconnect();
        process.exit(1)
    })

}
