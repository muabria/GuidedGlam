// TODO: seed the DB using Prisma
const prisma = require("./client");

async function seed() {
    console.log("Seeding the database.");
    await prisma.faceShape.deleteMany();



    // <------------------------ HOMEPAGE ------------------------>
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

        const round = await prisma.faceShape.create({
            data: {
                name: "Round"
            }
        })
        const oval = await prisma.faceShape.create({
            data: {
                name: "Oval"
            }
        })
        const square = await prisma.faceShape.create({
            data: {
                name: "Square"
            }
        })
        const triangle = await prisma.faceShape.create({
            data: {
                name: "Triangle"
            }
        })


        // <------------------------ SKIN TONE ------------------------>


        const fair = await prisma.skinTone.create({
            data: {
                name: "Fair"
            }
        })


        const light = await prisma.skinTone.create({
            data: {
                name: "Light"
            }
        })

        const lightMedium = await prisma.skinTone.create({
            data: {
                name: "Light Medium"
            }
        })
        const medium = await prisma.skinTone.create({
            data: {
                name: "Medium"
            }
        })
        const mediumDeep = await prisma.skinTone.create({
            data: {
                name: "Medium Dark"
            }
        })
        const dark = await prisma.skinTone.create({
            data: {
                name: "Dark"
            }
        })
        const darkDeep = await prisma.skinTone.create({
            data: {
                name: "Dark Deep"
            }
        })


        // <------------------------ SKIN TONE ------------------------>


        const dry = await prisma.skinType.create({
            data: {
                name: "Dry"
            }
        })


        const combo = await prisma.skinType.create({
            data: {
                name: "Combo"
            }
        })

        const oily = await prisma.skinType.create({
            data: {
                name: "Oily"
            }
        })
        const sensitive = await prisma.skinType.create({
            data: {
                name: "Sensitive"
            }
        })


    }



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



    // <------------------------ SKIN TONE ------------------------>



    // <---- SKIN TYPE: DRY ---->

    // <---- SKIN TYPE: OILY ---->

    // <---- SKIN TYPE: COMBO ---->

    // <---- SKIN TYPE: SENSITIVE ---->




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




