// TODO: seed the DB using Prisma
const prisma = require("./client");

async function seed() {
    console.log("Seeding the database.");
    await prisma.comment.deleteMany();
    await prisma.post.deleteMany();
    await prisma.user.deleteMany();
    await prisma.equipment.deleteMany();
    await prisma.category.deleteMany();


    // <------------------------ HOMEPAGE ------------------------>

    //<-------------------------------- CATEGORIES -------------------------------->

    try {
        const FaceShape = await prisma.category.create({
            data: {
                category: "Face Shapes"
            }
        })

        const SkinTones = await prisma.category.create({
            data: {
                category: "Skin Tones"
            }
        })

        const SkinTypes = await prisma.category.create({
            data: {
                category: "Skin Types"
            }
        })

    }


// <------------------------ FACE SHAPE ------------------------>



    // // <---- DIAMOND ---->
    // const Diamond = await prisma.equipment.create({
    //     data: {
    //         name: "",
    //         description: "",
    //         image: "",
    //         category: { connect: { id: Diamond.id } },
            
    //     },
    //     include: { category: true }
    // })


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
}
    seed().then(async () => {
        await prisma.$disconnect();
    }).catch(async (e) => {
        console.error(e)
        await prisma.$disconnect();
        process.exit(1)
    })



    
