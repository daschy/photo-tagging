import os
import shutil
import pytest
import pytest_asyncio
from models.ExifFileCRUD import ExifFileCRUD
# Replace `your_module` with the actual module name


class TestExifFileCRUD:
	test_keyword_list = [
		"Aalsmeer",
		"background",
		"black",
		"blue",
		"Meester Jac. Takkade",
		"Netherlands",
		"sky",
		"white",
		"windmill",
	]

	test_gps_lat = "52 deg 17' 25.78\" N"
	test_gps_lon = "4 deg 47' 46.24\" E"
	test_data_path = os.path.join(os.getcwd(), "tests", "test_data")

	@pytest_asyncio.fixture(scope="class")
	async def exif_crud(self):
		output = ExifFileCRUD()
		yield output

	@pytest_asyncio.fixture(scope="function")
	async def test_file_path_without_data(self, exif_crud: ExifFileCRUD):
		original_file_name = "windmill_address_some_none.NEF"
		original_test_file_path = os.path.join(self.test_data_path, original_file_name)
		copy_original_test_file_path = os.path.join(
			self.test_data_path,
			f"copy_without_data_{original_file_name}",
		)
		shutil.copyfile(original_test_file_path, copy_original_test_file_path)
		await exif_crud.delete_keyword_list(copy_original_test_file_path)
		yield copy_original_test_file_path
		if os.path.exists(copy_original_test_file_path):
			os.remove(copy_original_test_file_path)

	@pytest_asyncio.fixture(scope="function")
	async def test_file_path_with_data(
		self,
		exif_crud: ExifFileCRUD,
	):
		original_file_name = "windmill_address_some_none.NEF"
		original_test_file_path = os.path.join(self.test_data_path, original_file_name)
		copy_original_test_file_path = os.path.join(
			self.test_data_path,
			f"copy_with_data_{original_file_name}",
		)
		shutil.copyfile(original_test_file_path, copy_original_test_file_path)
		await exif_crud.save_keyword_list(
			copy_original_test_file_path, self.test_keyword_list
		)
		await exif_crud.save_gps_data(
			copy_original_test_file_path, self.test_gps_lat, self.test_gps_lon
		)
		yield copy_original_test_file_path
		if os.path.exists(copy_original_test_file_path):
			os.remove(copy_original_test_file_path)

	@pytest.mark.asyncio
	async def test_save_keyword_list(
		self, exif_crud: ExifFileCRUD, test_file_path_without_data: str
	):
		result = await exif_crud.save_keyword_list(
			test_file_path_without_data, self.test_keyword_list
		)
		assert result
		result = await exif_crud.read_keyword_list(test_file_path_without_data)
		assert result == self.test_keyword_list

	@pytest.mark.asyncio
	async def test_add_keyword_list(
		self, exif_crud: ExifFileCRUD, test_file_path_without_data: str
	):
		await exif_crud.delete_keyword_list(test_file_path_without_data)
		await exif_crud.add_keyword_list(
			test_file_path_without_data, [self.test_keyword_list[0]]
		)
		await exif_crud.add_keyword_list(
			test_file_path_without_data, self.test_keyword_list
		)
		result = await exif_crud.read_keyword_list(test_file_path_without_data)
		assert result == ([self.test_keyword_list[0]] + self.test_keyword_list)

	@pytest.mark.asyncio
	async def test_delete_keyword_list(
		self, exif_crud: ExifFileCRUD, test_file_path_with_data: str
	):
		await exif_crud.delete_keyword_list(test_file_path_with_data)
		file_keyword_list = await exif_crud.read_keyword_list(test_file_path_with_data)
		assert len(file_keyword_list) == 0

	@pytest.mark.asyncio
	async def test_read_keyword_list(
		self, exif_crud: ExifFileCRUD, test_file_path_with_data: str
	):
		result = await exif_crud.read_keyword_list(test_file_path_with_data)

		assert result == self.test_keyword_list

	@pytest.mark.asyncio
	async def test_save_gps_data(
		self, exif_crud: ExifFileCRUD, test_file_path_without_data: str
	):
		result = await exif_crud.save_gps_data(
			test_file_path_without_data, self.test_gps_lat, self.test_gps_lon
		)
		assert result is True

	@pytest.mark.asyncio
	async def test_read_gps_data(
		self, exif_crud: ExifFileCRUD, test_file_path_with_data: str
	):
		result = await exif_crud.read_gps_data(test_file_path_with_data)
		assert result == (self.test_gps_lat, self.test_gps_lon)
