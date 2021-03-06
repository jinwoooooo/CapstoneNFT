package com.capstone.capstonenft.ui.fragment.main

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Rect
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.activity.result.ActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.activityViewModels
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.capstone.capstonenft.R
import com.capstone.capstonenft.base.BaseFragment
import com.capstone.capstonenft.databinding.FragmentGalleryBinding
import com.capstone.capstonenft.system.utils.PixelUtil
import com.capstone.capstonenft.ui.activity.detail.GalleryDetailActivity
import com.capstone.capstonenft.ui.adapter.main.GalleryAdapter
import com.capstone.capstonenft.ui.adapter.main.ProfileAdapter
import com.capstone.capstonenft.viewmodel.MainViewModel
import java.io.InputStream

class GalleryFragment() : BaseFragment() {
    lateinit var mBinding: FragmentGalleryBinding
    lateinit var mGalleryAdapter: GalleryAdapter
    val mViewModel: MainViewModel by activityViewModels()
    private val imageActivityLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result: ActivityResult ->
            if (result.resultCode == AppCompatActivity.RESULT_OK) {
                mViewModel.getMainItem()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        mBinding = DataBindingUtil.inflate(inflater, R.layout.fragment_gallery, container, false)

        init()

        return mBinding.root
    }

    fun init() {

        mGalleryAdapter = GalleryAdapter(){ v, pos ->
            Intent(activity, GalleryDetailActivity::class.java).apply {
                this.putExtra("data", mViewModel.mldGallery.value!!.token[pos])
                imageActivityLauncher.launch(this)
            }
        }
        mBinding.fgRvGallery.adapter = mGalleryAdapter
        mBinding.fgRvGallery.layoutManager = LinearLayoutManager(mActivity, LinearLayoutManager.VERTICAL, false)

        mBinding.fgSlSwipe.setOnRefreshListener {
            mViewModel.getMainItem()
            mBinding.fgSlSwipe.isRefreshing = false
        }

        mViewModel.mldGallery.observe(viewLifecycleOwner){
            mGalleryAdapter.setItem(it.token)
        }
    }
}