-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "MakeupProduct" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "price" DOUBLE PRECISION NOT NULL,
    "userId" INTEGER,

    CONSTRAINT "MakeupProduct_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Comment" (
    "id" SERIAL NOT NULL,
    "content" TEXT NOT NULL,
    "userId" INTEGER NOT NULL,

    CONSTRAINT "Comment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Category" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "Category_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SkinTone" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "SkinTone_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SkinType" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "SkinType_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "FaceShape" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "FaceShape_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "_MakeupProductToSkinTone" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateTable
CREATE TABLE "_MakeupProductToSkinType" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateTable
CREATE TABLE "_CommentToMakeupProduct" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateTable
CREATE TABLE "_CategoryToMakeupProduct" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateTable
CREATE TABLE "_FaceShapeToMakeupProduct" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Category_name_key" ON "Category"("name");

-- CreateIndex
CREATE UNIQUE INDEX "SkinTone_name_key" ON "SkinTone"("name");

-- CreateIndex
CREATE UNIQUE INDEX "SkinType_name_key" ON "SkinType"("name");

-- CreateIndex
CREATE UNIQUE INDEX "FaceShape_name_key" ON "FaceShape"("name");

-- CreateIndex
CREATE UNIQUE INDEX "_MakeupProductToSkinTone_AB_unique" ON "_MakeupProductToSkinTone"("A", "B");

-- CreateIndex
CREATE INDEX "_MakeupProductToSkinTone_B_index" ON "_MakeupProductToSkinTone"("B");

-- CreateIndex
CREATE UNIQUE INDEX "_MakeupProductToSkinType_AB_unique" ON "_MakeupProductToSkinType"("A", "B");

-- CreateIndex
CREATE INDEX "_MakeupProductToSkinType_B_index" ON "_MakeupProductToSkinType"("B");

-- CreateIndex
CREATE UNIQUE INDEX "_CommentToMakeupProduct_AB_unique" ON "_CommentToMakeupProduct"("A", "B");

-- CreateIndex
CREATE INDEX "_CommentToMakeupProduct_B_index" ON "_CommentToMakeupProduct"("B");

-- CreateIndex
CREATE UNIQUE INDEX "_CategoryToMakeupProduct_AB_unique" ON "_CategoryToMakeupProduct"("A", "B");

-- CreateIndex
CREATE INDEX "_CategoryToMakeupProduct_B_index" ON "_CategoryToMakeupProduct"("B");

-- CreateIndex
CREATE UNIQUE INDEX "_FaceShapeToMakeupProduct_AB_unique" ON "_FaceShapeToMakeupProduct"("A", "B");

-- CreateIndex
CREATE INDEX "_FaceShapeToMakeupProduct_B_index" ON "_FaceShapeToMakeupProduct"("B");

-- AddForeignKey
ALTER TABLE "MakeupProduct" ADD CONSTRAINT "MakeupProduct_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Comment" ADD CONSTRAINT "Comment_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_MakeupProductToSkinTone" ADD CONSTRAINT "_MakeupProductToSkinTone_A_fkey" FOREIGN KEY ("A") REFERENCES "MakeupProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_MakeupProductToSkinTone" ADD CONSTRAINT "_MakeupProductToSkinTone_B_fkey" FOREIGN KEY ("B") REFERENCES "SkinTone"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_MakeupProductToSkinType" ADD CONSTRAINT "_MakeupProductToSkinType_A_fkey" FOREIGN KEY ("A") REFERENCES "MakeupProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_MakeupProductToSkinType" ADD CONSTRAINT "_MakeupProductToSkinType_B_fkey" FOREIGN KEY ("B") REFERENCES "SkinType"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_CommentToMakeupProduct" ADD CONSTRAINT "_CommentToMakeupProduct_A_fkey" FOREIGN KEY ("A") REFERENCES "Comment"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_CommentToMakeupProduct" ADD CONSTRAINT "_CommentToMakeupProduct_B_fkey" FOREIGN KEY ("B") REFERENCES "MakeupProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_CategoryToMakeupProduct" ADD CONSTRAINT "_CategoryToMakeupProduct_A_fkey" FOREIGN KEY ("A") REFERENCES "Category"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_CategoryToMakeupProduct" ADD CONSTRAINT "_CategoryToMakeupProduct_B_fkey" FOREIGN KEY ("B") REFERENCES "MakeupProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_FaceShapeToMakeupProduct" ADD CONSTRAINT "_FaceShapeToMakeupProduct_A_fkey" FOREIGN KEY ("A") REFERENCES "FaceShape"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_FaceShapeToMakeupProduct" ADD CONSTRAINT "_FaceShapeToMakeupProduct_B_fkey" FOREIGN KEY ("B") REFERENCES "MakeupProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;
