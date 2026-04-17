-- AlterTable
ALTER TABLE "_CategoryToMakeupProduct" ADD CONSTRAINT "_CategoryToMakeupProduct_AB_pkey" PRIMARY KEY ("A", "B");

-- DropIndex
DROP INDEX "_CategoryToMakeupProduct_AB_unique";

-- AlterTable
ALTER TABLE "_CommentToMakeupProduct" ADD CONSTRAINT "_CommentToMakeupProduct_AB_pkey" PRIMARY KEY ("A", "B");

-- DropIndex
DROP INDEX "_CommentToMakeupProduct_AB_unique";

-- AlterTable
ALTER TABLE "_FaceShapeToMakeupProduct" ADD CONSTRAINT "_FaceShapeToMakeupProduct_AB_pkey" PRIMARY KEY ("A", "B");

-- DropIndex
DROP INDEX "_FaceShapeToMakeupProduct_AB_unique";

-- AlterTable
ALTER TABLE "_MakeupProductToSkinTone" ADD CONSTRAINT "_MakeupProductToSkinTone_AB_pkey" PRIMARY KEY ("A", "B");

-- DropIndex
DROP INDEX "_MakeupProductToSkinTone_AB_unique";

-- AlterTable
ALTER TABLE "_MakeupProductToSkinType" ADD CONSTRAINT "_MakeupProductToSkinType_AB_pkey" PRIMARY KEY ("A", "B");

-- DropIndex
DROP INDEX "_MakeupProductToSkinType_AB_unique";
