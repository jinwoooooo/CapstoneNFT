package com.capstone.capstonenft.ui.activity.create

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.widget.Toast
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult
import androidx.activity.viewModels
import androidx.databinding.DataBindingUtil
import com.bumptech.glide.Glide
import com.capstone.capstonenft.NFT
import com.capstone.capstonenft.R
import com.capstone.capstonenft.base.BaseActivity
import com.capstone.capstonenft.databinding.ActivityCreateBinding
import com.capstone.capstonenft.dto.DialogItem
import com.capstone.capstonenft.system.utils.Trace
import com.capstone.capstonenft.ui.dialog.CommonDialog
import com.capstone.capstonenft.viewmodel.CreateViewModel
import java.io.*
import java.text.SimpleDateFormat
import java.util.*

class CreateActivity : BaseActivity() {
    lateinit var mBinding: ActivityCreateBinding
    lateinit var mResultLauncher: ActivityResultLauncher<Intent>
    private val mViewModel: CreateViewModel by viewModels()

    lateinit var uri: Uri
    lateinit var file: File

    private val imageActivityLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result: ActivityResult ->
            if (result.resultCode == RESULT_OK) {
                result.data?.let {
                    uri = it.data as Uri
                    Glide.with(this)
                        .load(uri)
                        .into(mBinding.fcIvImage)

                    val ins: InputStream? = uri.let {
                        applicationContext.contentResolver.openInputStream(it)
                    }

                    val img: Bitmap = BitmapFactory.decodeStream(ins)
                    file = createImageFile()
                    BitmapConvertFile(img, file.path)
                }
            }
        }
    private val simActivityLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result: ActivityResult ->
            if (result.resultCode == RESULT_OK) {
                finish()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mBinding = DataBindingUtil.setContentView(this, R.layout.activity_create)
        mBinding.listener = this

        mViewModel.token.observe(this) {
            CommonDialog(
                DialogItem(
                    title = "????????????",
                    content = "????????? ??????????????????."
                )
            ) { _ ->
                NFT.instance.loginResponse.token_list.add(it)
                setResult(RESULT_OK)
                finish()
            }.show(supportFragmentManager, "")
        }

        mViewModel.upload.observe(this) {
            Intent(this, ImageCheckActivity::class.java).apply {
                this.putExtra("data", it)
                simActivityLauncher.launch(this)
            }
        }
    }

    fun onClick(v: View) {
        when (v.id) {
            R.id.fc_iv_image -> {
                Intent(Intent.ACTION_PICK).apply {
                    this.type = MediaStore.Images.Media.CONTENT_TYPE
                    imageActivityLauncher.launch(this)
                }
            }

            R.id.fc_btn_regist -> {
                if (uri == null) {
                    CommonDialog(
                        DialogItem(
                            title = "???????????? ??????????????????",
                            content = "????????? ????????? ????????? ????????? ?????? ???????????? ??????????????????",
                            okBtnName = "??????"
                        )
                    ) {

                    }.show(supportFragmentManager, "")

                    return
                }

                if (file == null)
                    return

                if (mBinding.fcEtDescription.text.isNullOrEmpty())
                    return

                if (mBinding.fpEtName.text.isNullOrEmpty())
                    return

                mViewModel.uploadImage(
                    file,
                    mBinding.fpEtName.text.toString(),
                    mBinding.fcEtDescription.text.toString(),
                    "aaa",
                    1
                )
            }
        }
    }

    private fun createImageFile(): File {

        // ????????? ?????? ?????? ( blackJin_{??????}_ )
        val timeStamp: String = SimpleDateFormat("HHmmss").format(Date())
        val imageFileName = "file"
        // ???????????? ????????? ?????? ?????? ( blackJin )
        val storageDir: File =
            File(cacheDir.path)
        if (!storageDir.exists()) storageDir.mkdirs()
        // ??? ?????? ??????
        val image = File.createTempFile(imageFileName, ".png", storageDir)
        return image
    }

    private fun BitmapConvertFile(bitmap: Bitmap, strFilePath: String) {
        var file = File(strFilePath);
        // OutputStream ?????? -> bitmap???????????? OutputStream??? ?????? File??? ???????????? ??????
        var out: OutputStream? = null;
        try {
            // ?????? ?????????
            file.createNewFile();
            // OutputStream??? ????????? Stream??? ????????? ????????????
            out = FileOutputStream(file);
            // bitmap ??????
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, out);
        } catch (e: Exception) {
            e.printStackTrace();
        } finally {
            try {
                out?.close();
            } catch (e: IOException) {
                e.printStackTrace();
            }
        }
    }
}