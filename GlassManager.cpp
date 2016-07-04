// this file is covered by the General Public License version 2 or later
// please see GPL.html for more details and licensing issues
// copyright Etienne de Foras ( the author )  mailto: etienne.deforas@gmail.com

#include "GlassManager.h"
#include "Glass.h"
#include "MaterialAir.h"
#include "MaterialVacuum.h"
#include "MaterialWater.h"
#include "MaterialUnknow.h"
#include "MaterialIo.h"

#include <cassert>

GlassManager* GlassManager::_pGlassManager=0;

//////////////////////////////////////////////////////////////////////////////
GlassManager::GlassManager()
{
    _vGlass.push_back(new MaterialAir);
    _vGlass.push_back(new MaterialVacuum);
    _vGlass.push_back(new MaterialWater);
}
//////////////////////////////////////////////////////////////////////////////
GlassManager::~GlassManager()
{
    // TODO delete _vMaterial
}
//////////////////////////////////////////////////////////////////////////////
Glass* GlassManager::create(string sMaterial) const
{
    for(unsigned int i=0;i<_vGlass.size();i++)
    {
        if(_vGlass[i]->name()==sMaterial)
            return _vGlass[i]->clone();
    }

    //error case
    Glass* pM=new MaterialUnknow;
    pM->set_formulae("placeholder for "+sMaterial);
    return pM;
}
//////////////////////////////////////////////////////////////////////////////
void GlassManager::destroy(Glass* pMaterial)
{
    delete pMaterial;
}
//////////////////////////////////////////////////////////////////////////////
GlassManager& GlassManager::singleton()
{
    if(_pGlassManager==0)
        _pGlassManager= new GlassManager; //TODO delete at exit

    assert(_pGlassManager);
    return *_pGlassManager;
}
//////////////////////////////////////////////////////////////////////////////
void GlassManager::list_available(vector<string>& vsAvailable)
{
    vsAvailable.clear();
    for(unsigned int i=0;i<_vGlass.size();i++)
        vsAvailable.push_back(_vGlass[i]->name());
}
//////////////////////////////////////////////////////////////////////////////
bool GlassManager::load(string sFile)
{
    Glass* pMat=MaterialIo::load(sFile);
    if(pMat==0)
        return false;

    //TODO verifier existence avant ajout
    _vGlass.push_back(pMat);
    return true;
}
//////////////////////////////////////////////////////////////////////////////
unsigned int GlassManager::solid_color(string sMaterial)
{
    for(unsigned int i=0;i<_vGlass.size();i++)
    {
        if(_vGlass[i]->name()==sMaterial)
            return _vGlass[i]->solid_color();
    }
    return 0xffffff;
}
//////////////////////////////////////////////////////////////////////////////
void GlassManager::inject(Glass* pGlass) //take ownership of pGlass
{
  _vGlass.push_back(pGlass);
}
//////////////////////////////////////////////////////////////////////////////