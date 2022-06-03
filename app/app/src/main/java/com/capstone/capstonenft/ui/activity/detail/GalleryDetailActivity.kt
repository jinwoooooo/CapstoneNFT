package com.capstone.capstonenft.ui.activity.detail

import android.R.attr.button
import android.content.Intent
import android.os.Bundle
import android.view.ContextMenu
import android.view.MenuItem
import android.view.View
import androidx.activity.viewModels
import androidx.databinding.DataBindingUtil
import com.bumptech.glide.Glide
import com.capstone.capstonenft.NFT
import com.capstone.capstonenft.R
import com.capstone.capstonenft.base.BaseActivity
import com.capstone.capstonenft.databinding.ActivityGalleryDetailBinding
import com.capstone.capstonenft.dto.Token
import com.capstone.capstonenft.system.utils.Trace
import com.capstone.capstonenft.viewmodel.DetailViewModel


class GalleryDetailActivity: BaseActivity() {
    lateinit var mBinding: ActivityGalleryDetailBinding
    lateinit var item: Token
    private val mViewModel:DetailViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mBinding = DataBindingUtil.setContentView(this, R.layout.activity_gallery_detail)
        item = intent.getSerializableExtra("data") as Token
        mBinding.listener = this
        mBinding.data = item
        mBinding.isMine = item.owner == NFT.instance.loginResponse.name

        Glide.with(this)
            .load(item.imageSrc)
            .into(mBinding.agdIvPicture)

        registerForContextMenu(mBinding.agdIvOption)

        mViewModel.message.observe(this){
            setResult(RESULT_OK)
            finish()
        }
    }

    fun onClick(v:View){
        when(v.id){
            R.id.agd_iv_exit -> {
                finish()
            }

            R.id.agd_btn_buy -> {
                if(item.owner == NFT.instance.loginResponse.name){
                    mViewModel.soldItem(item.tokenId, price = 0)
//                    fun soldItem(tokenId: String, price: Int) {
                }else{
                    mViewModel.buyItem(item.tokenId.toString())
                }
            }

            R.id.agd_tv_owner -> {
                Intent(this, UserDetailActivity::class.java).apply {
                    this.putExtra("owner", item.owner)
                    startActivity(this)
                }
            }
        }
    }

    override fun onCreateContextMenu(
        menu: ContextMenu?,
        v: View?,
        menuInfo: ContextMenu.ContextMenuInfo?
    ) {
        super.onCreateContextMenu(menu, v, menuInfo)
        Trace.error("not if()")

        if (v === mBinding.agdIvOption) {
            Trace.error("if()")
            menuInflater.inflate(R.menu.context_menu, menu)
        }
    }

    override fun onContextItemSelected(menu: MenuItem): Boolean {
        mViewModel.setProfile(item.imageSrc)
        return super.onContextItemSelected(menu)
    }
}